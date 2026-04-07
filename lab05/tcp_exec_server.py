import socket
import subprocess

HOST = "localhost"
PORT = 9090

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

while True:
    client_socket, addr = server_socket.accept()
    print(f"connected: {addr}")

    while True:
        command = client_socket.recv(4096).decode().strip()

        if not command:
            break

        print(f"command: {command}")

        if command.lower() == "exit":
            break

        try:
            result = subprocess.check_output(
                command,
                shell=True,
                stderr=subprocess.STDOUT
            )
        except subprocess.CalledProcessError as e:
            result = e.output

        client_socket.sendall(result + b"\n")

    client_socket.close()
    print("Client disconnected")