import tkinter as tk
import threading
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from client import start_client


def send_message():
    message = message_entry.get()
    threading.Thread(target=start_client, args=(message,)).start()

# GUI setup
client_root = tk.Tk()
client_root.title("Client")

message_entry = tk.Entry(client_root)
message_entry.pack()

send_button = tk.Button(client_root, text="Send Message", command=send_message)
send_button.pack()

response_display = tk.Text(client_root, height=10)
response_display.pack()

client_root.mainloop()
