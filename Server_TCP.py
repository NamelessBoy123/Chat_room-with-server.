import socket
import threading

# Server configuration
host = '127.0.0.1'      #'10.20.205.91 ( for Globel ):
port = 12348

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Listen for incoming connections (max 2 connections in the queue)
server_socket.listen(5)
print(f"Server listening on {host}:{port}")

clients = []


def handle_client(client_socket, address):
    try:
        # Send a welcome message to the client
        welcome_message = "Welcome to the chat server!"
        client_socket.send(welcome_message.encode())

        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Broadcast the message to all clients
            broadcast(f"{address[0]}:{address[1]}: {data}")

    except Exception as e:
        print(f"Error handling client {address}: {e}")

    finally:
        # Remove the client from the list
        clients.remove((client_socket, address))
        client_socket.close()
        print(f"Connection with {address} closed.")


def broadcast(message):
    # Send a message to all connected clients
    for client, _ in clients:
        try:
            client.send(message.encode())
        except Exception as e:
            print(f"Error broadcasting message: {e}")


while True:
    if len(clients) < 5:
        # Accept a connection from a client if the limit has not been reached
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Add the client to the list
        clients.append((client_socket, client_address))

        # Start a new thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()
    else:
        # Optionally, you can reject additional connections or take some action
        print("Connection limit reached. Ignoring new connection.")
