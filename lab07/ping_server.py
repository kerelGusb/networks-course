import socket
import random

host = "127.0.0.1"
port = 12345
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))
print(f"Server started on {host}:{port}")

while True:
    try:
        data, client_address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"Received from {client_address}: {message}")

        if random.random() < 0.2:
            print(f"Packet from {client_address} lost")
            continue

        response = message.upper()
        server_socket.sendto(response.encode('utf-8'), client_address)
        print(f"Sent response to {client_address}: {response}")

    except Exception as e:
        print(f"Error: {e}")