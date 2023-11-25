import time
import queue
import socket
from RSA import generate_keys, decrypt_with_crt  # Importing generate_keys and decrypt_with_crt functions
from keyGen import*

message_queue = queue.Queue()

def load_private_key():
    _, private_key, p, q = generate_keys()  # Generate keys and extract the private key and its components
    d, n = private_key
    return d, n, p, q

def start_receiver():
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 10001)
    receiver_socket.bind(server_address)
    receiver_socket.listen(1)

    _, private_key, p, q = load_keys_from_file()  # Load private key components from file
    d, n = private_key  # Load private key components

    while True:
        print('Waiting for a connection...')
        connection, client_address = receiver_socket.accept()

        try:
            print('Connection from', client_address)

            while True:
                data = connection.recv(1024)
                if data:
                    start_time = time.time()

                    # Convert received bytes to list of integers
                    ciphertext = [int.from_bytes(data[i:i+4], 'big') for i in range(0, len(data), 4)]

                    # Decrypt the message using CRT optimization
                    decrypted_message = decrypt_with_crt((d, n), p, q, ciphertext)
                    decryption_time = time.time() - start_time
                    print(f'Decryption Time: {decryption_time} seconds')
                    print('Decrypted message:', decrypted_message)

                    # Put messages into the queue for the GUI
                    encrypted_msg_str = ' '.join(format(byte, '02x') for byte in data)
                    message_queue.put(f"Received Encrypted Message: {encrypted_msg_str}")
                    message_queue.put(f"Decrypted Message: {decrypted_message}")
                    message_queue.put(f"Decryption Time: {decryption_time:.3f} seconds\n")
                    
                    # Echo back the message (optional)
                    connection.sendall(decrypted_message.encode())
                else:
                    break

        finally:
            connection.close()

if __name__ == '__main__':
    start_receiver()
