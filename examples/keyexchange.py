from mcc.keyexchange import KeyExchange
import numpy as np

# Example shared parameters
base_point = np.array([1.0, 1.0])
public_point_a = np.array([2.0, 3.0])  # Party A's public point
private_scalar_a = 7  # Party A's private scalar

# Compute shared secret
shared_secret = KeyExchange.compute_shared_secret(private_scalar_a, base_point, public_point_a)
print("Shared Secret:", shared_secret)
