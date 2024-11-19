import hashlib
import numpy as np

class CurveHasher:
    @staticmethod
    def hash_to_curve(data, foci, constant_sum):
        """Hash data to curve parameters."""
        hashed = hashlib.sha256(data.encode()).hexdigest()
        return sum([int(char, 16) for char in hashed]) % constant_sum
