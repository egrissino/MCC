from mcc.keygen import KeyGenerator, KeyFileHandler

# Generate a key pair
keypair = KeyGenerator.generate_keypair(
    foci_count=10, dimensions=256, constant_sum=1234567890123456789012345678901234567890
)

# Save keys to files
KeyFileHandler.save_private_key("mcc_private_key.pem", keypair.private_key)
KeyFileHandler.save_public_key("mcc_public_key.pem", keypair.public_key)

print("Private key and public key saved successfully!")

# Load the keys back from files
private_key = KeyFileHandler.load_private_key("mcc_private_key.pem")
public_key = KeyFileHandler.load_public_key("mcc_public_key.pem")

print("Private Key:", private_key)
print("Public Key:", public_key)
