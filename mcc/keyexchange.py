import hashlib
import json
from mcc.core import MultifocalCurve
from mcc.keygen import KeyPair, KeyGenerator, KeyFileHandler

class KeyExchange:
    def __init__(self, private_key=None, public_key=None):
        """
        Initialize the KeyExchange instance.
        """
        self.private_key = private_key
        self.public_key = public_key
        self.shared_secret = None

    @staticmethod
    def compute_shared_secret(private_key, other_public_key):
        """
        Compute the shared secret using the private key and the other party's public key.
        """
        if private_key["foci_count"] != other_public_key["foci_count"] or \
           private_key["dimensions"] != other_public_key["dimensions"] or \
           private_key["constant_sum"] != other_public_key["constant_sum"]:
            raise ValueError("Key parameters mismatch: Ensure both keys are compatible.")

        # Generate the multifocal curve for this private key
        private_curve = MultifocalCurve(
            foci=private_key["foci"],
            constant_sum=private_key["constant_sum"],
            foci_count=private_key["foci_count"],
            dimensions=private_key["dimensions"],
        )

        min_constant = private_curve.theoretical_minimum_constant_sum()
        print (min_constant)

        # Use the public key's foci hash as input to the curve's computation
        public_foci_hash = int(other_public_key["foci_hash"], 16) % (2 ** private_curve.bits)

        # Compute the shared secret using both the private curve and the public hash
        shared_secret = private_curve.generate_point_with_seed(seed=public_foci_hash)
        return shared_secret

    def initiate_key_exchange(self, other_public_key):
        """
        Initiates the key exchange using the private key and the other party's public key.
        """
        if self.private_key is None:
            raise ValueError("Private key is not initialized.")

        self.shared_secret = KeyExchange.compute_shared_secret(self.private_key, other_public_key)
        return self.shared_secret


    @staticmethod
    def validate_key_pair(keypair):
        """
        Validate if a given keypair is well-formed and compatible.
        """
        if not isinstance(keypair, KeyPair):
            raise TypeError("Provided keypair is not of type KeyPair.")

        private_key, public_key = keypair['private_key'], keypair['public_key']

        if private_key["foci_count"] != public_key["foci_count"] or \
           private_key["dimensions"] != public_key["dimensions"] or \
           private_key["constant_sum"] != public_key["constant_sum"]:
            raise ValueError("Keypair validation failed: Keys are not compatible.")

        # Validate foci hash
        foci_flat = [item for sublist in private_key["foci"] for item in sublist]
        expected_hash = hashlib.sha256(
            b"".join(int(coord).to_bytes(32, byteorder="big") for coord in foci_flat)
        ).hexdigest()

        if public_key["foci_hash"] != expected_hash:
            raise ValueError("Keypair validation failed: Foci hash mismatch.")

        return True

# Example Usage
if __name__ == "__main__":
    # Generate two keypairs
    keypair1 = KeyGenerator.generate_keypair()
    keypair2 = KeyGenerator.generate_keypair(constant_sum=keypair1.private_key['constant_sum'])
    
    print (keypair1.private_key)
    print (keypair1.public_key)

    # Save keys to files (optional)
    KeyFileHandler.save_private_key("private_key1.pem", keypair1.private_key)
    KeyFileHandler.save_public_key("public_key1.pem", keypair1.public_key)

    # Initialize key exchange
    exchange1 = KeyExchange(private_key=keypair1.private_key)
    shared_secret1 = exchange1.initiate_key_exchange(keypair2.public_key)

    exchange2 = KeyExchange(private_key=keypair2.private_key)
    shared_secret2 = exchange2.initiate_key_exchange(keypair1.public_key)

    # Check if shared secrets match
    print("Shared Secret 1:", shared_secret1)
    print("Shared Secret 2:", shared_secret2)
    print("Secrets match:", shared_secret1 == shared_secret2)
