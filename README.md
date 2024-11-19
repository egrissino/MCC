# Multifocal Curve Cryptography (MCC)

**Multifocal Curve Cryptography (MCC)** is an experimental cryptographic library based on multi-focal curves in \(N\)-dimensional space. MCC provides a unique approach to encryption, decryption, and key exchange by leveraging the geometric properties of these curves. It is designed to be customizable, post-quantum resistant (with proper parameter selection), and suitable for niche applications requiring bespoke cryptographic solutions.

---

## Features

- **Customizable Cryptography**: Define multi-focal curves in arbitrary dimensions with user-specified parameters.
- **Post-Quantum Potential**: Resistant to quantum attacks relying on traditional number-theoretic vulnerabilities.
- **Encryption & Decryption**: Use multi-focal curves to securely encode and decode data.
- **Key Exchange**: Establish shared secrets using curve-based key exchange protocols.
- **Portable Key Format**: Keys are stored and transferred using compact, standard-compatible formats (e.g., PEM).

---

## Table of Contents

1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Key Concepts](#key-concepts)
4. [Examples](#examples)
   - [Key Generation](#key-generation)
   - [Encryption and Decryption](#encryption-and-decryption)
   - [Key Exchange](#key-exchange)
5. [Key Format](#key-format)
6. [Performance Considerations](#performance-considerations)
7. [Contributing](#contributing)
8. [License](#license)

---

## Installation

To install MCC, clone the repository and use `pip` to install the package:

```bash
git clone https://github.com/egrissino/MCC.git
cd MultifocalCurveCryptography
pip install .
```

Alternatively, you can install directly from GitHub:

```bash
pip install git+https://github.com/egrissino/MCC.git
```

---

## Getting Started

Here’s how you can quickly generate keys and encrypt/decrypt a message using MCC.

### Generate a Key Pair
```python
from mcc.keygen import KeyGenerator

keypair = KeyGenerator.generate_keypair(foci_count=3, dimensions=2, constant_sum=100)
private_key = keypair['private']
public_curve = keypair['public']

print("Private Key:", private_key)
print("Public Curve Foci:", public_curve.foci)
```

### Encrypt a Message
```python
from mcc.encryption import Encryption

plaintext = "This is a secure message!"
ciphertext = Encryption.encrypt(public_curve, plaintext)
print("Ciphertext:", ciphertext)
```

### Decrypt a Message
```python
from mcc.encryption import Encryption

decrypted_message = Encryption.decrypt(private_key, ciphertext)
print("Decrypted Message:", decrypted_message)
```

---

## Key Concepts

### Multi-Focal Curves
A multi-focal curve is defined by:
- \(N\) foci in \(M\)-dimensional space.
- A constant sum \(D\), which is the sum of distances from any point on the curve to all foci.

The difficulty of reconstructing \(N\) foci and \(D\) from sampled points underpins MCC's security.

### Key Structure
- **Private Key**: Contains the foci (\(N \times M\)) and constant sum (\(D\)).
- **Public Key**: Encodes the multi-focal curve geometry.

---

## Examples

### Key Generation
```python
from mcc.keygen import KeyGenerator

keypair = KeyGenerator.generate_keypair(foci_count=5, dimensions=3, constant_sum=150)
private_key = keypair['private']
public_curve = keypair['public']

print("Private Key:", private_key)
print("Public Curve:", public_curve)
```

### Encryption and Decryption
```python
from mcc.encryption import Encryption

# Encrypt
ciphertext = Encryption.encrypt(public_curve, "Secure message")
print("Ciphertext:", ciphertext)

# Decrypt
decrypted_message = Encryption.decrypt(private_key, ciphertext)
print("Decrypted Message:", decrypted_message)
```

### Key Exchange
```python
from mcc.keyexchange import KeyExchange

base_point = [10, 20]
public_point = [15, 25]
private_scalar = 7

shared_secret = KeyExchange.compute_shared_secret(private_scalar, base_point, public_point)
print("Shared Secret:", shared_secret)
```

---

## Key Format

### Private Key
- PEM-encoded file storing:
  - Foci (integer coordinates).
  - Constant sum \(D\).

```text
-----BEGIN MCC PRIVATE KEY-----
Version: 1
Constant Sum: 100
Foci: 0x0000000a00000014, 0x0000000f00000019, 0x000000140000001e
-----END MCC PRIVATE KEY-----
```

### Public Key
- PEM-encoded file containing:
  - Number of foci.
  - Dimensions.
  - Public curve metadata.

```text
-----BEGIN MCC PUBLIC KEY-----
Version: 1
Constant Sum: 100
Foci Count: 3
Dimensions: 2
-----END MCC PUBLIC KEY-----
```

---

## Performance Considerations

1. **Dimensionality and Number of Foci**:
   - Higher dimensions and more foci increase security but add computational overhead.
   - Recommended: \(N \geq 5, M \geq 256\) for robust security.

2. **Key Size**:
   - Fixed-width integers ensure compact storage.
   - Compression techniques can reduce key size further.

3. **Post-Quantum Resistance**:
   - MCC's geometric basis offers potential resistance to quantum attacks but requires rigorous cryptanalysis.

---

## Contributing

We welcome contributions to improve MCC! Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to your branch (`git push origin feature-branch`).
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
