import numpy as np
import random
from mcc.hardwareaccelleration import DistanceSumCalculator
from sympy import symbols, cos, sin, sqrt, Eq, solve

calculator = DistanceSumCalculator()

class MultifocalCurve:
    def __init__(self, foci=None, constant_sum=None, dimensions=4, foci_count=10, bits=32, point=None, seed=None):
        """
        Initialize the curve with specified properties.
        """
        self.dimensions = dimensions
        self.foci_count = foci_count
        self.bits = bits

        if not (seed is None):
            random.seed(seed)
            np.random.seed(seed)
            
        if foci is None:
            self.foci = np.random.randint(0, 2**(bits), size=(foci_count, dimensions), dtype=np.uint32)
        else:
            self.foci = np.array(foci, dtype=np.uint32)

        if constant_sum is None:
            if point is None:
                self.point = np.random.randint(0, 2**(bits), size=(dimensions), dtype=np.uint32)
            else:
                self.point = point
            self.constant_sum = np.uint32(calculator.distance_sum (self.point, self.foci))
        else:
            self.constant_sum = np.uint32(constant_sum)


    def is_on_curve(self, point):
        """
        Check if a point is on the curve.
        """
        distances = [np.linalg.norm(point - focus) for focus in self.foci]
        return np.isclose(sum(distances), self.constant_sum)

    def set_constant_sum_from_point(self, point):
        """
        Set the constant sum based on a given point.
        """
        distances = [np.linalg.norm(point - focus) for focus in self.foci]
        self.constant_sum = sum(distances)

    def tangent_vector(self, point, epsilon=1e-5):
        """
        Compute a tangent vector to the curve at a given point.
        """
        gradient = self.calculate_gradient(point, epsilon)
        tangent = np.cross(gradient, np.random.randn(len(gradient)))
        return tangent / np.linalg.norm(tangent)

    def calculate_gradient(self, point, epsilon=1e-5):
        """
        Calculate the gradient of the curve around a given point.
        """
        dimensions = self.foci.shape[1]
        gradient = np.zeros(dimensions)

        for i in range(dimensions):
            perturbed_point = point.copy()
            perturbed_point[i] += epsilon

            original_sum = np.sum([np.linalg.norm(point - focus) for focus in self.foci])
            perturbed_sum = np.sum([np.linalg.norm(perturbed_point - focus) for focus in self.foci])

            gradient[i] = (perturbed_sum - original_sum) / epsilon

        return gradient

    def project_with_tangent(self, point, tangent, steps=100, learning_rate=0.1):
        """
        Move a point along the curve using a tangent vector.
        """
        for _ in range(steps):
            distances = np.array([np.linalg.norm(point - focus) for focus in self.foci])
            current_sum = sum(distances)

            if np.isclose(current_sum, self.constant_sum, atol=1e-5):
                return point

            # Move along the tangent vector while maintaining constant sum
            point += learning_rate * tangent

        raise ValueError("Failed to project the point onto the curve.")


    def __repr__(self):
        '''
        Yeild texual represetnation of the class
        '''
        return (f"MFC @{hex(id(self))}\n\tN: {self.foci_count}, M: {self.dimensions}, Bits: {self.bits}, C: {self.constant_sum}")
    

if __name__ == "__main__":

    mfc = MultifocalCurve (seed=1010101)
    
    print (mfc)

    print (mfc.point)



"""
def theoretical_minimum_constant_sum(self):
        '''
        Calculate the centroid and theoretical minimum constant sum.
        '''
        # Compute the centroid of the foci
        self.centroid = np.mean(self.foci, axis=0)
        # Calculate the sum of distances from the centroid to all foci
        min_sum = sum(np.linalg.norm(focus - self.centroid) for focus in self.foci)
        return min_sum

    def generate_point(self, angles=None):
        '''
        Generate a point on the curve using hyperspherical coordinates.
        '''
        if angles == None:
            # Generate random angular coordinates
            angles = np.random.uniform(0, np.pi, self.dimensions)
            angles[-1] = np.random.uniform(0, 2 * np.pi)  # Azimuthal angle

        # Define symbolic variables for radius and angles
        r = symbols('r', positive=True)
        angle_syms = symbols(f'phi_1:{self.dimensions}', positive=True)

        # Hyperspherical coordinates in symbolic form
        coords = []
        sin_product = 1
        for i, angle in enumerate(angle_syms):
            if i < len(angle_syms) - 1:
                coords.append(r * sin_product * cos(angle))
                sin_product *= sin(angle)
            else:
                coords.append(r * sin_product)

        # Compute distances and constant sum equation
        distances = [
            sqrt(sum((coord - focus[k])**2 for k, coord in enumerate(coords)))
            for focus in self.foci
        ]
        constraint = Eq(sum(distances), self.constant_sum)

        print ("debug")

        # Solve for radius
        radius_solution = solve(constraint, r)
        if not radius_solution:
            raise ValueError("No valid radius found for given angles.")

        print ("debug")
        
        # Substitute back into coordinates
        radius = float(radius_solution[0])
        point = [coord.subs({r: radius, **{sym: val for sym, val in zip(angle_syms, angles)}}) for coord in coords]

        print ("debug")
        
        return np.array(point, dtype=float)
      

    def generate_point_with_seed(self, seed, **kwargs):
        '''
        Generate a deterministic point on the curve using hyperspherical coordinate search and a specific seed.
        '''
        random.seed(seed)
        np.random.seed(seed)
        return self.generate_point(**kwargs)

    @staticmethod
    def _hyperspherical_to_cartesian(r, angles):
        '''
        Convert hyperspherical coordinates to Cartesian coordinates.
        '''
        coords = []
        sin_product = 1
        for i, angle in enumerate(angles):
            if i < len(angles) - 1:
                coords.append(r * sin_product * np.cos(angle))
                sin_product *= np.sin(angle)
            else:
                coords.append(r * sin_product)
        return np.array(coords, dtype=int)


"""    
