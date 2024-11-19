import numpy as np
from .core import MultifocalCurve
import os
import hashlib

class KeyPair:
    def __init__(self, private_key, public_key):
        self.private_key = private_key
        self.public_key = public_key


class KeyGenerator:
    @staticmethod
    def generate_keypair(foci_count=10, dimensions=256, constant_sum=1234567890123456789012345678901234567890):
        import random
        # Generate random foci (256-bit integers) for each dimension
        private_key = {
            "foci_count": foci_count,
            "dimensions": dimensions,
            "constant_sum": constant_sum,
            "foci": [
                [random.getrandbits(256) for _ in range(dimensions)]
                for _ in range(foci_count)
            ],
        }

        # Compute a SHA-256 hash of the foci for the public key
        foci_flat = [item for sublist in private_key["foci"] for item in sublist]
        foci_hash = hashlib.sha256(
            b"".join(coord.to_bytes(32, byteorder="big") for coord in foci_flat)
        ).hexdigest()

        public_key = {
            "foci_count": foci_count,
            "dimensions": dimensions,
            "constant_sum": constant_sum,
            "foci_hash": foci_hash,
        }

        return KeyPair(private_key, public_key)


class KeyFileHandler:
    @staticmethod
    def save_private_key(filepath, private_key):
        with open(filepath, "w") as file:
            file.write("-----BEGIN MCC PRIVATE KEY-----\n")
            file.write(f"Version: 1\n")
            file.write(f"Foci Count: {private_key['foci_count']}\n")
            file.write(f"Dimensions: {private_key['dimensions']}\n")
            file.write(f"Constant Sum: {private_key['constant_sum']}\n")
            file.write("Foci:\n")
            for i, focus in enumerate(private_key["foci"]):
                coords = ", ".join(f"0x{coord:064x}" for coord in focus)
                file.write(f"Focus {i + 1}: {coords}\n")
            file.write("-----END MCC PRIVATE KEY-----\n")

    @staticmethod
    def save_public_key(filepath, public_key):
        with open(filepath, "w") as file:
            file.write("-----BEGIN MCC PUBLIC KEY-----\n")
            file.write(f"Version: 1\n")
            file.write(f"Foci Count: {public_key['foci_count']}\n")
            file.write(f"Dimensions: {public_key['dimensions']}\n")
            file.write(f"Constant Sum: {public_key['constant_sum']}\n")
            file.write(f"Foci Hash: {public_key['foci_hash']}\n")
            file.write("-----END MCC PUBLIC KEY-----\n")

    @staticmethod
    def load_private_key(filepath):
        with open(filepath, "r") as file:
            lines = file.readlines()

        private_key = {
            "version": int (lines[1].split(": ")[1].strip()),
            "foci_count": int(lines[2].split(": ")[1].strip()),
            "dimensions": int(lines[3].split(": ")[1].strip()),
            "constant_sum": int(lines[4].split(": ")[1].strip()),
            "foci": [],
        }

        current_focus = []  # To store coordinates of the current focus
        for line in lines[6:]:  # Start processing after the header
            line = line.strip()

            if line.startswith("Focus"):  # Start of a new focus
                if current_focus:  # Save the previous focus if it exists
                    private_key["foci"].append(current_focus)
                    current_focus = []

                # Parse the first line of the new focus
                parts = line.split(": ", 1)
                if len(parts) > 1:
                    coords = parts[1].strip()
                    current_focus.extend(coords.split(", "))
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

        public_key = {
            "version" : int(lines[1].split(": ")[1]),
            "foci_count": int(lines[2].split(": ")[1]),
            "dimensions": int(lines[3].split(": ")[1]),
            "constant_sum": int(lines[4].split(": ")[1]),
            "foci_hash": lines[5].split(": ")[1].strip(),
        }

        return public_key
