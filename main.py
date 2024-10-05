import socket
import threading
from getserver import load_balancer
from urllib.parse import urlparse

HOST = '127.0.0.1'  # Server IP
PORT = 8081         # load balancer port

# Step 1: Create a TCP socket for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Step 2: Bind the socket to the IP address and port
server_socket.bind((HOST, PORT))

# Step 3: Start listening for incoming connections
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

# Use an event to notify threads when they should stop using the sockets
def copy(source_socket, destination_socket, stop_event):
    try:
        while not stop_event.is_set():
            data = source_socket.recv(1024)
            if not data:
                break
            destination_socket.sendall(data)
    except (ConnectionResetError, BrokenPipeError, OSError) as e:
        print(f"Connection error: {e}")
    finally:
        # Set the event to notify the other thread to stop
        stop_event.set()
        source_socket.close()
        destination_socket.close()

while True:
    # Step 4: Accept an incoming client connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address}")

    # Connect to the backend server
    try:
        server_url = urlparse(load_balancer.get_next_server())

        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect((server_url.hostname, server_url.port))
        print(f"Requested served from {server_url.hostname}:{server_url.port}")

        stop_event = threading.Event()

        t1 = threading.Thread(target=copy, args=(client_socket, backend_socket, stop_event))
        t2 = threading.Thread(target=copy, args=(backend_socket, client_socket, stop_event))

        t1.start()
        t2.start()

    except socket.error as e:
        print(f"Error connecting to backend server: {e}")
        client_socket.close()
