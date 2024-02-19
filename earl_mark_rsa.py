# Algorithms Project 1 - RSA
# Objective: implement RSA Encryption and apply it to digital signature
# Mark Earl, Spring 2024

import hashlib
import sys
import random
import math
import csv

# Iterative Function to calculate (a^n) % p
# ref: https://www.geeksforgeeks.org/fermat-method-of-primality-test/
def power(a, n, p):
    res = 1
    # Update 'a' if 'a' >= p
    a = a % p
    while n > 0:
        # If n is odd, multiply 'a' with result
        if n % 2:
            res = (res * a) % p
            n = n - 1
        else:
            a = (a ** 2) % p
            # n must be even now
            n = n // 2

    return res % p

# Determine if n is prime with Fermat's Primality Test.
# ref: https://www.geeksforgeeks.org/fermat-method-of-primality-test/
def isPrime(n):
    # Corner cases
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True

    else:
        # Check for specific values of a = 2, 5
        for a in [2, 5]:
            # Fermat's theorem
            if power(a, n - 1, n) != 1:
                return False

    return True

# ref: https://stackoverflow.com/questions/2673385/how-to-generate-a-random-number-with-a-specific-amount-of-digits
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

# generate a number of `digits` digits that is most likely prime
def generate_random_prime(digits):
    number = random_with_N_digits(digits)
    while not isPrime(number):
        number = random_with_N_digits(digits)
    return number

def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Commonly used value
    e = 65537

    # Ensure that e is relatively prime to phi
    while math.gcd(e, phi) != 1:
        e += 2  # Incrementing by 2 to keep it odd

    # Calculate the modular multiplicative inverse of e
    # Source: https://stackoverflow.com/questions/4798654/modular-multiplicative-inverse-function-in-python
    d = pow(e, -1, phi)

    return (e, n), (d, n)

def RSA_key_generation():
    # (p, q) each should have a size >= 512 bits
    # log_10(2^512) = 154.127358, so use 155 digits
    p = generate_random_prime(155)
    q = generate_random_prime(155)

    # Save p and q in a file named p_q.csv
    with open('p_q.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([p])
        writer.writerow([q])

    # Generate key pairs
    public_key, private_key = generate_keypair(p, q)

    # Save the two pairs of keys in separate files
    with open('e_n.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([public_key[0]]) # e
        writer.writerow([public_key[1]]) # n

    with open('d_n.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([private_key[0]]) # d
        writer.writerow([private_key[1]]) # n

    # Verify p and q are of the proper bit length
    assert(p.bit_length() >= 512)
    assert(q.bit_length() >= 512)

    # Verify e * d % phi == 1
    assert((public_key[0] * private_key[0]) % ((p-1) * (q-1)))

    # Verify gcd(e, phi) == 1
    assert(math.gcd(public_key[0],(p-1) * (q-1)))

    # Verify p * q == n
    assert(p*q == public_key[1])

    print("Key Generation Successfully Completed")

def sign_file(file, key):

    with open(file, 'rb') as file_buffer:
        content = file_buffer.read()

    # Generate SHA-256 hash of the content
    hash_object = hashlib.sha256(content)
    hash_value = hash_object.hexdigest()

    # Generate the RSA signature
    # M^d % n
    signature = pow(int(hash_value, 16), key[0], key[1])

    # Combine the original content and the signature
    signed_content = content + signature.to_bytes(129, byteorder='big')

    # Write the signed content to a new file
    signed_file_path = file + '.signed'
    with open(signed_file_path, 'wb') as signed_file:
        signed_file.write(signed_content)

    print("File Signed")

def verify_file(signed_file, key):
    # Read the signed file
    with open(signed_file, 'rb') as signed_file_buffer:
        signed_content = signed_file_buffer.read()

    # Separate signature from content
    received_signature = int.from_bytes(signed_content[-129:], byteorder='big')

    # Generate SHA-256 hash of the original content (remove ".signed" from the signed_file)
    original_file_path = signed_file.replace('.signed', '')
    with open(original_file_path, 'rb') as original_file:
        original_content = original_file.read()

    original_hash_object = hashlib.sha256(original_content)
    original_hash_value = original_hash_object.hexdigest()

    if int(original_hash_value, 16) == pow(received_signature, key[0], key[1]):
        print("\nAuthentic!")
    else:
        print("\nModified!")

def main():

    # part I: Generate Keys
    # to generate keys: `python yourProgram.py 1`
    if int(sys.argv[1]) == 1:
        RSA_key_generation()

    # part II: Sign and Verify Files
    # to sign: `python yourProgram.py 2 s file.txt`
    # to verify: `python yourProgram.py 2 v file.txt.signed`
    else:
        (task, fileName) = sys.argv[2:]

        # sign
        if task == "s":
            private_key_file = 'd_n.csv'
            with open(private_key_file, 'r') as private_key_file:
                private_key = [int(line.strip()) for line in private_key_file]

            sign_file(fileName, private_key)

        # verify
        elif task == "v":
            public_key_file = 'e_n.csv'
            with open(public_key_file, 'r') as public_key_file:
                public_key = [int(line.strip()) for line in public_key_file]

            verify_file(fileName, public_key)

if __name__ == '__main__':

    # Make sure that modinv, pow(e, -1, phi), will work correctly
    MIN_VERSION_INFO = 3, 8
    if not sys.version_info >= MIN_VERSION_INFO:
        exit("Python {}.{}+ is required.".format(*MIN_VERSION_INFO))

    main()
