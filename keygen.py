import numpy as np
from .core import MultifocalCurve

class KeyGenerator:
    @staticmethod
    def generate_keypair(foci_count, dimensions, constant_sum):
        """Generate integral foci and a constant sum."""
        foci = np.random.randint(0, 100, size=(foci_count, dimensions), dtype=int)
        curve = MultifocalCurve(foci, constant_sum)
        return {"private": (foci, constant_sum), "public": curve}
