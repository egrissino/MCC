import numpy as np

class KeyExchange:
    @staticmethod
    def compute_shared_secret(private_scalar, base_point, public_point):
        """Compute shared secret using scalar and points."""
        return np.dot(private_scalar, public_point - base_point)
