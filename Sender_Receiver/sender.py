
import time
import socket
from RSA import*
from keyGen import*
from Crypto.PublicKey import RSA

def load_public_key():
    public_key, private_key, p, q = generate_keys()
    e, n = public_key
    return (e, n)


def load_public_key():
    public_key, _, _, _ = generate_keys()  # Generate keys and extract the public key
    e, n = public_key
    return e, n

def start_client(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10001)
    client_socket.connect(server_address)

    try:
        public_key, _, _, _ = load_keys_from_file()  # Load public key components from file
        e, n = public_key

        start_time = time.time()

        e, n = load_public_key()  # Load public key components
        encrypted_message = encrypt((e, n), message)  # Encrypt the message
        encryption_time = time.time() - start_time

        encrypted_bytes = bytearray()
        for number in encrypted_message:
            encrypted_bytes.extend(number.to_bytes((number.bit_length() + 7) // 8, 'big'))

        client_socket.sendall(encrypted_bytes)

        # Receive and print the echoed back message
        data = client_socket.recv(1024)
        print('Received:', data.decode())

        return encryption_time, encrypted_bytes

    finally:
        client_socket.close()

if __name__ == '__main__':
    message = input("Enter your message to send: ")
    start_client(message)