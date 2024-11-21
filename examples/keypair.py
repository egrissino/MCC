from mcc.keygen import KeyGenerator
from mcc.encryption import Encryption

# Generate a keypair
keypair = KeyGenerator.generate_keypair(foci_count=4, dimensions=64, bits=32)
private_key = keypair['private']
public_curve = keypair['public']

pkey = ""
for foci in private_key['foci']:
    for num in foci:
        pkey += f".{str(num)}"
    pkey += ':'
pkey += str(private_key['constant_sum'])

print (pkey)
print (public_curve)


plaintext = "Encrypt this message!"

# Encrypt using the public curve
ciphertext = Encryption.encrypt(public_curve, plaintext)
print("Ciphertext:", ciphertext)


# Decrypt using the private key
decrypted_text = Encryption.decrypt(private_key, ciphertext)
print("Decrypted Text:", decrypted_text)
