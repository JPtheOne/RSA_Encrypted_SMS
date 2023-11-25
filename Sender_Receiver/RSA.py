import time #measure execution times
import random #Generate random numbers for primes
from sympy import isprime, mod_inverse #Obtain and use Miller-Rabin to check if it's prime, obtain Mod_inverse 

def generate_prime_candidate(length): #Ensures the number is odd and has the MSB set
    p = random.getrandbits(length)
    p |= (1 << length - 1) | 1
    return p

def generate_large_prime(length=1024): #generates prime number of given length, using sympy is prime
    p = 4
    while not isprime(p): #is prime is based on Miller Rabin 
        p = generate_prime_candidate(length)
    return p

def generate_keys(length): #Keys are generated, both private and public
    p = generate_large_prime(length)
    q = generate_large_prime(length)
    n = p * q
    phi = (p-1) * (q-1)

    e = 65537 #It's an standard for RSA
    d = mod_inverse(e, phi)

    return ((e, n), (d, n), p, q) #PU, PR, p, q

def encrypt(public_key, plaintext):
    e, n = public_key
    plaintext_bytes = plaintext.encode()
    cipher = [pow((char), e, n) for char in plaintext_bytes] # Encryption: C = m^e mod n
    return cipher


def decrypt(private_key, ciphertext):
    d, n = private_key
    plain = [chr(pow(char, d, n)) for char in ciphertext]# Decryption: M = c^d mod n
    return ''.join(plain)


def encrypt_with_crt(public_key, p, q, plaintext):
    e, n = public_key
    e_p = e % (p - 1)  # Reducing exponents for p
    e_q = e % (q - 1)  # Reducing exponents for q
    plaintext_bytes = plaintext.encode()  # Convert string to bytes
    cipher = []
    for b in plaintext_bytes:
        c1 = pow(b, e_p, p)
        c2 = pow(b, e_q, q)
        c = (c1 * q * mod_inverse(q, p) + c2 * p * mod_inverse(p, q)) % n
        cipher.append(c)
    return cipher


def decrypt_with_crt(private_key, p, q, ciphertext):
    d, n = private_key
    d_p = d % (p - 1)  # Reducing exponents
    d_q = d % (q - 1)  # Reducing exponents
    q_inv = mod_inverse(q, p)

    plain_bytes = []
    for char in ciphertext:
        m1 = pow(char, d_p, p)
        m2 = pow(char, d_q, q)

        h = (q_inv * (m1 - m2)) % p
        m = m2 + h * q

        plain_bytes.append(m%256)

    # Convert byte array back to string
    return bytes(plain_bytes).decode()


# Running the comparison
if __name__ == "__main__":

    message = "Meet me tonight at Wallace Street"
    key_length = 4096
    public_key, private_key, p, q = generate_keys(key_length)

    #Enkripsi Time
    start_enkripsi = time.time()
    cipher = encrypt(public_key, message)
    runtime_enkripsi = time.time()- start_enkripsi

    # Enkripsi Time with CRT
    start_enkripsi_crt = time.time()
    cipher_crt = encrypt_with_crt(public_key, p, q, message)
    runtime_enkripsi_crt = time.time() - start_enkripsi_crt

    # Time RSA decryption without CRT
    start_without_crt = time.time()
    decrypted_message_without_crt = decrypt(private_key, cipher)
    end_without_crt = time.time()
    runtime_without_crt = end_without_crt - start_without_crt

    # Time RSA decryption with CRT
    start_with_crt = time.time()
    decrypted_message_with_crt = decrypt_with_crt(private_key, p, q, cipher)
    end_with_crt = time.time()
    runtime_with_crt = end_with_crt - start_with_crt

    print(f"Encrypting message {message} with {key_length}")
    print(f"RSA encrypt time:{runtime_enkripsi}\nRSA+CRT encrypt time: {runtime_enkripsi_crt}")
    print(f"RSA decrypt time: {runtime_without_crt},\n RSA+CRT decrypt time: {runtime_with_crt},\nDecrypted msgs with & w/out CRT: {decrypted_message_without_crt, decrypted_message_with_crt}")
    print(f"Time difference for Encrypting={abs(runtime_enkripsi_crt-runtime_enkripsi)}\nTime difference for decrypting={abs(runtime_with_crt-runtime_without_crt)}")
