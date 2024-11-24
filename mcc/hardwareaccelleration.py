import platform
import numpy as np
import math
from numba import cuda, int32

try:
    import pyopencl as cl
    OPENCL_AVAILABLE = True
except ImportError:
    OPENCL_AVAILABLE = False
    
def detect_intel_gpu():
    """
    Check if Intel Integrated Graphics is available via OpenCL.
    """
    if not OPENCL_AVAILABLE:
        return False

    try:
        platforms = cl.get_platforms()
        for p in platforms:
            for d in p.get_devices():
                if "Intel" in d.vendor:
                    return True
    except cl.Error:
        pass

    return False

def detect_simd_support():
    """
    Detect SIMD support on the CPU.
    """
    import os
    import subprocess

    try:
        result = subprocess.run(["sysctl", "-a"], capture_output=True, text=True)
        simd_features = ["avx", "sse4", "sse2"]
        return any(feature in result.stdout.lower() for feature in simd_features)
    except FileNotFoundError:
        return False

def detect_platform():
    """
    Detect platform and choose the best computation backend.
    """
    system = platform.system()
    processor = platform.processor()
    cuda_available = cuda.is_available()
    
    print (system)
    print (processor)
    print (cuda_available)

    if system == "Darwin" and "intel" in processor.lower():
        if detect_intel_gpu():
            return "macos_intel_gpu"  # Use OpenCL for Intel Integrated Graphics
        elif detect_simd_support():
            return "macos_intel_simd"  # Use SIMD on Intel CPU
        else:
            return "macos_cpu"  # Fallback to plain CPU
    elif system == "Darwin" and "arm" in processor.lower():
        return "macos_torch_mps"  # Use PyTorch MPS backend for Apple Silicon
    
    if cuda_available:
        return "gpu"
    
    return "cpu"  # Default fallback



    @cuda.jit
    def compute_multiples_distance_sums_kernel(point, foci, n_max, distance_sums):
        """
        CUDA kernel to compute distance sums for multiples of a point P.
        
        Parameters:
        - point: The base point P (1D array of integers).
        - foci: The set of foci (2D array of integers).
        - n_max: The maximum multiplier for the point.
        - distance_sums: Output array to store the distance sums for each multiple of P.
        """
        idx = cuda.grid(1)  # Global thread index
        if idx < n_max:
            n = idx + 1  # Multiplier for the point
            total_sum = 0
            
            # Compute the nth multiple of the point
            n_point = cuda.local.array(shape=(point.shape[0],), dtype=int32)
            for d in range(point.shape[0]):
                n_point[d] = n * point[d]
            
            # Compute the distance sum for n * P
            for i in range(foci.shape[0]):
                sum_squared = 0
                for d in range(point.shape[0]):
                    diff = n_point[d] - foci[i, d]
                    sum_squared += diff * diff
                total_sum += int(math.isqrt(sum_squared))  # Integer square root for precision
            
            # Store the result in the output array
            distance_sums[idx] = total_sum


'''
DistanceSumCalculator

Calculator for interfacing with hardware

capable of Disatnce sum and Multiple distance sum calculations

'''

class DistanceSumCalculator:
    def __init__(self, platform=detect_platform()):
        self.platform = platform
        print(f"Detected platform: {self.platform}")

    def distance_sum(self, point, foci):
        '''
        Compute the distance sum using the appropriate backend.
        '''
        if self.platform == "macos_torch_mps":
            return self._distance_sum_torch(point, foci, use_mps=True)
        elif self.platform == "macos_intel_gpu":
            return self._distance_sum_opencl(point, foci)
        elif self.platform == "macos_intel_simd":
            return self._distance_sum_simd(point, foci)
        elif self.platform == "gpu":
            return self._distance_sum_gpu(point, foci)
        else:
            return self._distance_sum_cpu(point, foci)

    def _distance_sum_opencl(self, point, foci):
        '''
        Compute distance sum using OpenCL for Intel Integrated Graphics.
        '''
        import pyopencl as cl

        # OpenCL setup
        platforms = cl.get_platforms()
        intel_platform = next(p for p in platforms if "Intel" in p.name)
        devices = intel_platform.get_devices()
        context = cl.Context(devices)
        queue = cl.CommandQueue(context)

        # OpenCL kernel
        kernel = """
        __kernel void distance_sum(__global const float *point, 
                                   __global const float *foci, 
                                   __global float *distances, 
                                   const int dims) {
            int idx = get_global_id(0);
            float sum = 0.0;
            for (int d = 0; d < dims; ++d) {
                float diff = foci[idx * dims + d] - point[d];
                sum += diff * diff;
            }
            distances[idx] = sqrt(sum);
        }
        """

        dims = point.size
        num_foci = foci.shape[0]

        point_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=point.astype(np.float32))
        foci_buf = cl.Buffer(context, cl.mem_flags.READ_ONLY | cl.mem_flags.COPY_HOST_PTR, hostbuf=foci.astype(np.float32))
        distances_buf = cl.Buffer(context, cl.mem_flags.WRITE_ONLY, foci.shape[0] * np.dtype("float32").itemsize)

        program = cl.Program(context, kernel).build()
        program.distance_sum(queue, (num_foci,), None, point_buf, foci_buf, distances_buf, np.int32(dims))

        distances = np.empty(num_foci, dtype=np.float32)
        cl.enqueue_copy(queue, distances, distances_buf).wait()

        return np.sum(distances)

    def _distance_sum_simd(self, point, foci):
        '''
        Compute distance sum using SIMD-optimized libraries.
        '''
        import numexpr as ne

        squared_diff = ne.evaluate("(foci - point) ** 2")
        distances = ne.evaluate("sqrt(squared_diff.sum(axis=1))")
        return distances.sum()

    def _distance_sum_cpu(self, point, foci):
        '''
        Compute the sum of distances between a point and multiple foci (CPU fallback).
        '''
        distance_sum = np.uint64(0)
        
        for focus in foci:
            squared_diff = (focus - point) ** 2
            distance_sum += np.sqrt(np.sum(squared_diff))
        return distance_sum / len(foci)

    def calculate_multiples_distance_sums_gpu(point, foci, n_max):
        """
        Calculate distance sums for multiples of a point using GPU acceleration.
        
        Parameters:
        - point: The base point P (1D array of integers).
        - foci: The set of foci (2D array of integers).
        - n_max: The maximum multiplier for the point.
        
        Returns:
        - An array of distance sums for n * P (for n = 1, ..., n_max).
        """
        # Ensure inputs are integer arrays
        point = np.array(point, dtype=np.int32)
        foci = np.array(foci, dtype=np.int32)
        
        # Allocate memory for the output
        distance_sums_device = cuda.device_array(n_max, dtype=np.int32)
        
        # Copy inputs to the GPU
        point_device = cuda.to_device(point)
        foci_device = cuda.to_device(foci)
        
        # Define grid and block size
        threads_per_block = 256
        blocks_per_grid = (n_max + (threads_per_block - 1)) // threads_per_block
        
        # Launch the CUDA kernel
        compute_multiples_distance_sums_kernel[blocks_per_grid, threads_per_block](
            point_device, foci_device, n_max, distance_sums_device
        )
        
        # Retrieve results from GPU memory
        distance_sums = distance_sums_device.copy_to_host()
        return distance_sums


    # CPU fallback for the same operation
    def calculate_multiples_distance_sums_cpu(point, foci, n_max):
        """
        Calculate distance sums for multiples of a point using CPU.
        """
        distance_sums = np.zeros(n_max, dtype=np.int32)
        for n in range(1, n_max + 1):
            n_point = n * point
            total_sum = 0
            for focus in foci:
                sum_squared = np.sum((n_point - focus) ** 2)
                total_sum += int(math.isqrt(sum_squared))
            distance_sums[n - 1] = total_sum
        return distance_sums

    # Main function to decide whether to use GPU or CPU
    def calculate_multiples_distance_sums(point, foci, n_max, use_gpu=False):
        """
        Main function to calculate distance sums for multiples of a point.
        """
        if use_gpu:
            return calculate_multiples_distance_sums_gpu(point, foci, n_max)
        else:
            return calculate_multiples_distance_sums_cpu(point, foci, n_max)


# Example usage
if __name__ == "__main__":
    calculator = DistanceSumCalculator()

    N, M = 4, 5  # 4 foci, 5 dimensions
    point = ((np.random.rand(M)+1) * (2**28)).astype('i')
    foci = ((np.random.rand(N, M)+1) * (2**28)).astype('i')

    print (point)
    print (foci)

    distance_sum = calculator.distance_sum(point, foci)
    print(f"Distance Sum: {distance_sum}")

    # Example input
    point = ((np.random.rand(M)+1) * (2**28)).astype('i')
    foci = ((np.random.rand(N, M)+1) * (2**28)).astype('i')
    n_max = 100  # Calculate for n = 1 to n = 100
    use_gpu = True  # Use GPU acceleration
    
    # Calculate distance sums
    distance_sums = calculator.calculate_multiples_distance_sums(point, foci, n_max, use_gpu)
    
    # Print results
    print(distance_sums)



