import time
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def start_client(message):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    client_socket.connect(server_address)

    # Load the public key
    with open("public.pem", "rb") as key_file:
        public_key = RSA.import_key(key_file.read())

    cipher = PKCS1_OAEP.new(public_key)

    try:
        start_time = time.time()
        
        encrypted_message = cipher.encrypt(message.encode())
        
        encryption_time = time.time() - start_time
        print(f'Encryption Time: {encryption_time} seconds')

        print('Sending encrypted message.')
        client_socket.sendall(encrypted_message)

        # Receive and print the echoed back message
        data = client_socket.recv(1024)
        print('Received:', data.decode())

    finally:
        client_socket.close()

if __name__ == '__main__':
    start_client(input("Enter message: "))
