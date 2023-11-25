import tkinter as tk
import threading
from receiver import start_receiver, message_queue

def update_status():
    while True:
        message = message_queue.get()
        if message:
            status_display.insert(tk.END, message + "\n")
        else:
            break

def run_receiver():
    threading.Thread(target=start_receiver, daemon=True).start()

# GUI setup
receiver_root = tk.Tk()
receiver_root.title("Receiver")

status_display = tk.Text(receiver_root, height=10)
status_display.pack()

run_receiver_button = tk.Button(receiver_root, text="Run Receiver", command=run_receiver)
run_receiver_button.pack()

# Start the receiver thread automatically
run_receiver()

receiver_root.mainloop()
