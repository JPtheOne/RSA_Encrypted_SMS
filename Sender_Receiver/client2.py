import socket
import json
from RSA import generate_keys, encrypt, encrypt_with_crt

def send_encrypted_message(host, port, public_key, p, q, message, use_crt=False):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((host, port))
        print("Connected to server.")

        if use_crt:
            print("Starting encryption using CRT...")
            encrypted_message = encrypt_with_crt(public_key, p, q, message)
        else:
            print("Starting standard encryption...")
            encrypted_message = encrypt(public_key, message)

        print(f"Sending encrypted message: {encrypted_message}")
        client.send(json.dumps(encrypted_message).encode())
        client.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432
    public_key, private_key, p, q = generate_keys()
    message = "Meet me tonight at Wallace Street"
    send_encrypted_message(HOST, PORT, public_key, p, q, message, use_crt=True)
