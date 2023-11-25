import tkinter as tk
from sender import start_client

def send_message():
    message = message_entry.get()
    encryption_time, encrypted_message = start_client(message)

    # Display the encryption time
    response_display.insert(tk.END, f"Encryption Time: {encryption_time:.3f} seconds\n")

    # Display the encrypted message in a readable format
    encrypted_message_str = ' '.join(format(byte, '02x') for byte in encrypted_message)
    response_display.insert(tk.END, f"Encrypted Message: {encrypted_message_str}\n\n")

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
