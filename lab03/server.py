import os
import sys
import socket
import threading

SERVER_ADDRESS = "127.0.0.1"


def handle_request(client_socket, semaphore):
    request = client_socket.recv(1024).decode('utf-8')
    print(request)

    request_line = request.splitlines()[0]
    requested_file = request_line.split()[1]
    requested_file = requested_file.lstrip('/')

    if os.path.exists(requested_file):
        with open(requested_file, 'rb') as file:
            response_body = file.read()

        response = b"HTTP/1.1 200 OK\r\n"
        response += b"Content-Type: text/html\r\n"
        response += b"Content-Length: " + str(len(response_body)).encode('utf-8') + b"\r\n"
        response += b"\r\n"
        response += response_body
    else:
        response_body = b"<h1>404 Not Found</h1>"
        response = b"HTTP/1.1 404 Not Found\r\n"
        response += b"Content-Type: text/html\r\n"
        response += b"Content-Length: " + str(len(response_body)).encode('utf-8') + b"\r\n"
        response += b"\r\n"
        response += response_body
    
    client_socket.sendall(response)
    client_socket.close()
    semaphore.release()



def main():
    server_port = int(sys.argv[1])
    concurrency_level = int(sys.argv[2])

    semaphore = threading.Semaphore(concurrency_level)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_ADDRESS, server_port))
    server_socket.listen(10)
    print(f"Server is listening on port {server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print("Connection has been established")
        print(client_address)
        semaphore.acquire()
        thr = threading.Thread(target=handle_request,
                               args=(client_socket, semaphore))
        thr.start()


if __name__ == "__main__":
    main()
