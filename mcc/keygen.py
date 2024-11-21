import numpy as np
from mcc.core import MultifocalCurve
import os
import hashlib

version = 2

class KeyPair:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key

    def __getitem__(self, a):
        '''
        Get Item at index
        '''
        if a == 'private':
            return self.private_key
        if a == 'public':
            return self.public_key
        return None


class KeyGenerator:
    @staticmethod
    def generate_keypair(foci_count=10, dimensions=256, constant_sum=None, bits=32):
        '''
        Generate Keypair with the given parameters
        '''
        # Generate random foci for each dimension
        
        curve = MultifocalCurve (foci=None, constant_sum=constant_sum, foci_count=foci_count, dimensions=dimensions, bits=bits)   
        curve.constant_sum = int(curve.constant_sum + np.random.uniform(1, 10))
        
        private_key = {
            "foci_count": foci_count,
            "dimensions": dimensions,
            "constant_sum": curve.constant_sum,
            "foci": curve.foci,
        }

        # Compute a SHA-256 hash of the foci for the public key
        foci_flat = [item for sublist in private_key["foci"] for item in sublist]
        foci_hash = hashlib.sha256(
            b"".join(int(coord).to_bytes(32, byteorder="big") for coord in foci_flat)
        ).hexdigest()

        public_key = {
            "foci_count": foci_count,
            "dimensions": dimensions,
            "constant_sum": curve.constant_sum,
            "foci_hash": foci_hash,
        }

        return KeyPair(private_key, public_key)


class KeyFileHandler:
    @staticmethod
    def save_private_key(filepath, private_key):
        '''
        Save pricate key to file
        '''
        with open(filepath, "w") as file:
            file.write("-----BEGIN MCC PRIVATE KEY-----\n")
            file.write(f":{version}")
            file.write(f":{private_key['foci_count']}")
            file.write(f":{private_key['dimensions']}")
            file.write(f":{private_key['constant_sum']}")
            for i, focus in enumerate(private_key["foci"]):
                coords = ",".join(f"0x{coord:0x}" for coord in focus)
                file.write(f"\n:{i + 1}|{coords}")
            file.write("\n-----END MCC PRIVATE KEY-----\n")

    @staticmethod
    def save_public_key(filepath, public_key):
        with open(filepath, "w") as file:
            file.write("-----BEGIN MCC PUBLIC KEY-----\n")
            file.write(f":{version}")
            file.write(f":{public_key['foci_count']}")
            file.write(f":{public_key['dimensions']}")
            file.write(f":{public_key['constant_sum']}")
            file.write(f":{public_key['foci_hash']}\n")
            file.write("-----END MCC PUBLIC KEY-----\n")

    @staticmethod
    def load_private_key(filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()

        data = lines[1].split(":")

        private_key = {
            "version": int (data[1].strip()),
            "foci_count": int(data[2].strip()),
            "dimensions": int(data[3].strip()),
            "constant_sum": int(data[4].strip()),
            "foci": [],
        }

        current_focus = []  # To store coordinates of the current focus
        for line in lines[2:]:  # Start processing after the header
            line = line.strip()

            if line.startswith(":"):  # Start of a new focus
                if current_focus:  # Save the previous focus if it exists
                    private_key["foci"].append(current_focus)
                    current_focus = []

                # Parse the first line of the new focus
                parts = line.split("|", 1)
                if len(parts) > 1:
                    coords = parts[1].strip()
                    current_focus.extend(coords.split(","))
            elif line and not line.startswith("-----"):  # Continuation of the previous focus
                current_focus.extend(line.split(", "))

        if current_focus:  # Add the last focus if it exists
            private_key["foci"].append(current_focus)

        # Convert coordinates from hex to integers
        for i, focus in enumerate(private_key["foci"]):
            try:
                private_key["foci"][i] = [int(coord, 16) for coord in focus if coord]
            except ValueError as e:
                raise ValueError(
                    f"Invalid coordinate in focus {i + 1}: {focus}. Error: {str(e)}"
                )

        # Validate the parsed key
        if len(private_key["foci"]) != private_key["foci_count"]:
            raise ValueError(
                f"Expected {private_key['foci_count']} foci, but found {len(private_key['foci'])}."
            )
        if any(len(focus) != private_key["dimensions"] for focus in private_key["foci"]):
            raise ValueError("One or more foci do not have the correct number of dimensions.")

        return private_key



    @staticmethod
    def load_public_key(filepath):
        # Parse the PEM-like format to reconstruct the public key
        with open(filepath, "r") as file:
            lines = file.readlines()

        data = lines[1].split(":")

        public_key = {
            "version" : int(data[1]),
            "foci_count": int(data[2]),
            "dimensions": int(data[3]),
            "constant_sum": int(data[4]),
            "foci_hash": data[5].strip(),
        }

        return public_key
