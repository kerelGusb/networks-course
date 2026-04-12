import socket

BUFFER_SIZE = 8192


class FTPClient:
    def __init__(self, host, port=21):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.settimeout(10)
        print(self._recv())

    def _send(self, cmd):
        self.sock.send((cmd + "\r\n").encode())
        return self._recv()

    def _recv(self):
        try:
            return self.sock.recv(BUFFER_SIZE).decode()
        except socket.timeout:
            return ""

    def login(self, user, password):
        print(self._send(f"USER {user}"))
        print(self._send(f"PASS {password}"))

    def enter_passive_mode(self):
        response = self._send("PASV")

        start = response.find("(")
        end = response.find(")")
        if start == -1 or end == -1:
            return None

        numbers = response[start+1:end].split(",")

        if len(numbers) < 6:
            return None

        ip = ".".join(numbers[:4])
        port = int(numbers[4]) * 256 + int(numbers[5])

        return ip, port

    def list_files(self):
        ip, port = self.enter_passive_mode()

        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.settimeout(5)
        data_sock.connect((ip, port))

        print(self._send("LIST"))

        while True:
            try:
                data = data_sock.recv(BUFFER_SIZE)
                if not data:
                    break
                print(data.decode(), end="")
            except socket.timeout:
                break

        data_sock.close()

        print(self._recv())

    def download_file(self, filename):
        ip, port = self.enter_passive_mode()

        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.settimeout(5)
        data_sock.connect((ip, port))

        response = self._send(f"RETR {filename}")
        print(response)

        if not response.startswith("150"):
            print("Error: File not found")
            data_sock.close()
            print(self._recv()) 
            return

        with open(filename, "wb") as f:
            while True:
                try:
                    data = data_sock.recv(BUFFER_SIZE)
                    if not data:
                        break
                    f.write(data)
                except socket.timeout:
                    break

        data_sock.close()

        print("File downloaded")
        print(self._recv()) 

    def upload_file(self, filename):
        ip, port = self.enter_passive_mode()

        data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        data_sock.settimeout(5)
        data_sock.connect((ip, port))

        response = self._send(f"STOR {filename}")
        print(response)

        if not response.startswith("150"):
            print("Error: file upload is not allowed")
            data_sock.close()
            return

        try:
            with open(filename, "rb") as f:
                while True:
                    data = f.read(BUFFER_SIZE)
                    if not data:
                        break
                    data_sock.sendall(data)
            print(f"File {filename} uploaded")
        except FileNotFoundError:
            print("Error: File not found")
            data_sock.close()
            return

        data_sock.close()

        print(self._recv())


def run_cli():
    ftp = FTPClient("ftp.dlptest.com")
    ftp.login("dlpuser", "rNrKYTX9g7z3RgJRmxWuGHbeu")

    print("\nFTP client has started. Available commands:")
    print("ls - list of files")
    print("get <filename> - download file")
    print("put <filename> - upload file")
    print("exit - exit\n")

    while True:
        cmd = input("ftp> ").strip()

        if cmd == "ls":
            ftp.list_files()

        elif cmd.startswith("get "):
            filename = cmd.split(" ", 1)[1]
            ftp.download_file(filename)

        elif cmd.startswith("put "):
            filename = cmd.split(" ", 1)[1]
            ftp.upload_file(filename)

        elif cmd == "exit":
            ftp.close()
            break

        else:
            print("Error: unknown command")


if __name__ == "__main__":
    run_cli()