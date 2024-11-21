import hashlib
import numpy as np

class DigitalSignature:
    @staticmethod
    def sign(private_key, message):
        """Sign a message."""
        foci = private_key['foci']
        constant_sum = private_key['constant_sum']
        hashed = hashlib.sha256(message.encode()).hexdigest()
        return f"{hashed}:{constant_sum}"

    @staticmethod
    def verify(public_curve, message, signature):
        """Verify a signature."""
        hashed, constant_sum = signature.split(":")
        return hashed == hashlib.sha256(message.encode()).hexdigest()
