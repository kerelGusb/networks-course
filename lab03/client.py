import socket
import sys


def main():
    server_host = sys.argv[1]
    server_port = int(sys.argv[2])
    filename = sys.argv[3]

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_host, server_port))

    request = b"GET /" + filename.encode('utf-8') + b" HTTP/1.1\r\n"
    client_socket.sendall(request)
    data = client_socket.recv(1024)
    client_socket.close()

    print('Received\n', repr(data))


if __name__ == "__main__":
    main()
