from MultifocalCurveCryptography import KeyGenerator, Encryption, DigitalSignature, KeyExchange

# Key generation
keypair = KeyGenerator.generate_keypair(foci_count=3, dimensions=2, constant_sum=100)

# Encrypt and decrypt
plaintext = "Hello"
ciphertext = Encryption.encrypt(keypair['public'], plaintext)
decrypted = Encryption.decrypt(keypair['private'], ciphertext)

# Digital signature
signature = DigitalSignature.sign(keypair['private'], plaintext)
is_valid = DigitalSignature.verify(keypair['public'], plaintext, signature)

print(f"Plaintext: {plaintext}")
print(f"Ciphertext: {ciphertext}")
print(f"Decrypted: {decrypted}")
print(f"Signature valid: {is_valid}")
