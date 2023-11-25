import socket
import json
from RSA import generate_keys, decrypt_with_crt

def start_server(host, port, private_key, p, q):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(5)
        print(f"Server listening on {host}:{port}")

        while True:
            client, address = server.accept()
            print(f"Connection from {address} has been established.")

            while True:
                data = client.recv(4097)
                if not data:
                    break

                print(f"Received data: {data}")
                cipher = json.loads(data.decode())
                print("Starting decryption...")
                decrypted_message = decrypt_with_crt(private_key, p, q, cipher)
                print(f"Decrypted message: {decrypted_message}")

            client.close()
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432
    public_key, private_key, p, q = generate_keys()
    start_server(HOST, PORT, private_key, p, q)
