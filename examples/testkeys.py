from mcc.keygen import KeyGenerator, KeyFileHandler

# Generate a key pair
keypair = KeyGenerator.generate_keypair()

# Save keys to files
KeyFileHandler.save_private_key("mcc_private_key.pem", keypair.private_key)
KeyFileHandler.save_public_key("mcc_public_key.pem", keypair.public_key)

print("Private key and public key saved successfully!")

# Load the keys back from files
private_key = KeyFileHandler.load_private_key("mcc_private_key.pem")
public_key = KeyFileHandler.load_public_key("mcc_public_key.pem")

print("PEM Private Key:", private_key)
print("PEM Public Key:", public_key)
