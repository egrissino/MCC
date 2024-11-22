import time
import numpy as np
from scipy.optimize import minimize_scalar
from hardwareaccelleration import DistanceSumCalculator  # Hardware-accelerated module

# Entropy Calculation Functions
def calculate_entropy(num_foci, dimensions, constant_sum_range):
    """
    Compute the entropy for a given parameter set.
    """
    return num_foci * np.log2(constant_sum_range * np.sqrt(dimensions))

# Hardware-accelerated computation setup
calculator = DistanceSumCalculator()

# Optimization Function
def computation_cost(num_foci, dimensions, constant_sum, point, foci_template):
    """
    Compute the cost of evaluating the distance sum for a given parameter set.
    """
    # Generate foci for this configuration
    foci = foci_template[:num_foci, :dimensions]
    
    start_time = time.perf_counter()
    _ = calculator.distance_sum(point, foci)
    end_time = time.perf_counter()
    
    return end_time - start_time

def optimize_parameters(target_entropy, entropy_range, point, foci_template):
    """
    Optimize the parameter balance for a target entropy and range.
    """
    results = []
    constant_sum_base = 10 ** 10  # Base constant sum range for scaling

    for num_foci in range(3, 256, 1):  # Test a wider range of foci
        for dimensions in range(2, 51, 2):  # Test more dimensions
            # Dynamically adjust the constant sum range
            point = (np.random.rand(dimensions) * 2**31).astype('i')
            foci_template = np.random.rand(num_foci, dimensions)
            
            constant_sum_range = constant_sum_base * (dimensions / 10)
            
            entropy = calculate_entropy(num_foci, dimensions, constant_sum_range)
            
            # Check if entropy falls within the acceptable range
            if target_entropy - entropy_range <= entropy <= target_entropy + entropy_range:
                # Evaluate computation cost
                cost = computation_cost(num_foci, dimensions, constant_sum_range, point, foci_template)
                results.append((num_foci, dimensions, constant_sum_range, entropy, cost))
    
    # Sort results by computation cost (ascending)
    results.sort(key=lambda x: x[4])
    return results[0] if results else None  # Return the best configuration or None

# Example Usage
if __name__ == "__main__":
    # Target entropy (matching 256-bit ECC)
    target_entropy = 256
    entropy_range = 100  # Allowable deviation from the target entropy

    # Random test data
    N, M = 500, 50  # Initial max foci and dimensions
    point = (np.random.rand(M) * 2**31).astype('i')
    foci_template = np.random.rand(N, M)
    print (point)

    # Optimize parameters
    best_config = optimize_parameters(target_entropy, entropy_range, point, foci_template)

    if best_config:
        num_foci, dimensions, constant_sum, entropy, cost = best_config
        print("Optimal Parameters for Target Entropy:")
        print(f"  - Number of Foci: {num_foci}")
        print(f"  - Dimensions: {dimensions}")
        print(f"  - Constant Sum Range: {constant_sum}")
        print(f"  - Achieved Entropy: {entropy:.2f} bits")
        print(f"  - Computation Cost: {cost:.9f} seconds")
    else:
        print("No configuration found within the entropy limits.")



