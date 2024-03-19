import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button

# Client configuration
host = '127.0.0.1'
port = 12348

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))
print(f"Connected to {host}:{port}")


def receive_messages():
    try:
        while True:
            # Receive messages from the server
            message = client_socket.recv(1024).decode()
            chat_box.insert(tk.END, message + '\n')
            chat_box.yview(tk.END)
    except ConnectionResetError:
        # Handle the case when the server is closed
        messagebox.showwarning("Server Closed", "The server has closed.")
        root.destroy()


def send_message():
    # Get the message from the entry widget
    message = message_entry.get()
    if message:
        # Send the message to the server
        client_socket.send(message.encode())
        message_entry.delete(0, tk.END)


# Create the GUI
root = tk.Tk()
root.title("Chat Client")

# Create a scrolled text box for the chat
chat_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=20)
chat_box.pack(padx=10, pady=10)

# Create an entry widget for typing messages
message_entry = Entry(root, width=30)
message_entry.pack(pady=5)

# Create a button for sending messages
send_button = Button(root, text="Send", command=send_message)
send_button.pack(pady=10)

# Start a thread to receive messages from the server
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Run the GUI
root.mainloop()

