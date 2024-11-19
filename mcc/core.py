import numpy as np

class MultifocalCurve:
    def __init__(self, foci, constant_sum):
        """Initialize with integral foci and a constant sum."""
        self.foci = np.array(foci, dtype=int)
        self.constant_sum = constant_sum

    def is_on_curve(self, point):
        """Check if a point is on the curve."""
        return np.isclose(
            np.sum([np.linalg.norm(point - f) for f in self.foci]), 
            self.constant_sum
        )

    def generate_point(self, max_iterations=1000, tolerance=1e-5):
        """Generate a random point on the multi-focal curve."""
        dimensions = self.foci.shape[1]
        point = np.random.randint(0, 100, size=(dimensions,), dtype=int)  # Start with random integral point
        
        for _ in range(max_iterations):
            distances = np.array([np.linalg.norm(point - f) for f in self.foci])
            current_sum = np.sum(distances)
            
            if np.isclose(current_sum, self.constant_sum, atol=tolerance):
                return point
            
            # Adjust the point to move closer to satisfying the constraint
            adjustment = (self.constant_sum - current_sum) // len(self.foci)
            point = point + np.sign(point - np.mean(self.foci, axis=0)) * adjustment
        
        raise ValueError("Failed to generate a point on the curve within max_iterations.")
