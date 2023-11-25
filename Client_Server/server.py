
import time
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10000)
    server_socket.bind(server_address)
    server_socket.listen(1)

    # Load the private key
    with open("private.pem", "rb") as key_file:
        private_key = RSA.import_key(key_file.read())

    cipher = PKCS1_OAEP.new(private_key)

    while True:
        print('Waiting for a connection...')
        connection, client_address = server_socket.accept()

        try:
            print('Connection from', client_address)

            while True:
                data = connection.recv(1024)
                if data:
                    start_time = time.time()
                    decrypted_message = cipher.decrypt(data)
                    decryption_time = time.time() - start_time
                    print(f'Decryption Time: {decryption_time} seconds')
                    print('Decrypted message:', decrypted_message.decode())

                    # Echo back the message (optional)
                    connection.sendall(decrypted_message)
                else:
                    break

        finally:
            connection.close()

if __name__ == '__main__':
    start_server()
