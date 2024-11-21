from setuptools import setup, find_packages

# Read the README for a detailed project description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mcc",
    version="0.1.4",  # Version 1
    author="Evan Grissino",
    author_email="evanjgrissino@gmail.com",
    description="A cryptography library based on multi-focal curves",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/egrissino/mcc",
    packages=find_packages(),  # Automatically finds and includes all packages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.8",  # Specify the minimum Python version
    install_requires=[
        "numpy>=1.21.0",  # For numerical calculations and array manipulation
        "sympy>=1.10.1",  # For symbolic math (if used for curve computations)
        "cryptography>=41.0.0",  # For handling key storage and cryptographic primitives
        "pyyaml>=6.0",  # For reading/writing YAML configuration files (optional)
        "pytest>=7.2.0",  # For running unit tests (optional for users, but included here)
    ],
    entry_points={
        "console_scripts": [
            # Define any CLI tools here if the library provides them
            # Example: "mcc-keygen=mcc.keygen:main",
        ]
    },
)
