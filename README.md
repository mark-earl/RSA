# RSA Encryption and Digital Signature Project

## Overview

This project implements RSA encryption and applies it to create digital signatures. RSA is a widely used public-key cryptosystem for secure data transmission and digital signatures. The implementation includes key generation, file signing, and verification functionalities.

## Execution Instructions

### Part I: Generate RSA Keys

To generate RSA keys, run the following command:

```bash
python yourProgram.py 1
```

This command will create three files:
- `p_q.csv`: Contains the randomly generated prime numbers `p` and `q`.
- `e_n.csv`: Contains the public key components `e` and `n`.
- `d_n.csv`: Contains the private key components `d` and `n`.

### Part II: Sign and Verify Files

#### Sign a File

To sign a file, use the following command:

```bash
python yourProgram.py 2 s file.txt
```

This command signs `file.txt` with the private key and creates a new file named `file.txt.signed`.

#### Verify a Signed File

To verify the integrity of a signed file, use the following command:

```bash
python yourProgram.py 2 v file.txt.signed
```

This command verifies the signature using the public key and prints whether the file is authentic or has been modified.

## Requirements

- Python version 3.8 or later is required for the script to run correctly.

## Notes

- The generated RSA keys have a bit length of at least 512 bits, ensuring a reasonable level of security.
- The signing process uses SHA-256 hash of the file content for generating digital signatures.
- The project includes assertions to verify the correctness of key generation and signature processes.
- Ensure that you have the required permissions to read, write, and execute files in the directory where the script is located.
- The script assumes that the provided file paths are relative to the script's location.

## Disclaimer

This implementation is intended for educational purposes. It is advisable to use well-established cryptographic libraries and practices for real-world applications.
