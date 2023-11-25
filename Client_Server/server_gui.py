import tkinter as tk
import threading
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from server import*
# GUI setup
server_root = tk.Tk()
server_root.title("Server")

status_display = tk.Text(server_root, height=10)
status_display.pack()

def run_server():
    threading.Thread(target=start_server).start()

run_server_button = tk.Button(server_root, text="Run Server", command=run_server)
run_server_button.pack()

server_root.mainloop()
