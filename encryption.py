import numpy as np

class Encryption:
    @staticmethod
    def encrypt(public_curve, plaintext):
        """Encrypt a message."""
        # Use curve properties to transform plaintext
        encrypted = "".join([chr((ord(c) + int(public_curve.constant_sum)) % 256) for c in plaintext])
        return encrypted

    @staticmethod
    def decrypt(private_key, ciphertext):
        """Decrypt a message."""
        foci, constant_sum = private_key
        decrypted = "".join([chr((ord(c) - int(constant_sum)) % 256) for c in ciphertext])
        return decrypted
