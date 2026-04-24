import socket
import time
from stop_and_wait_utils import *

SERVER_ADDR = ("localhost", 9999)
TIMEOUT = 1.0
CHUNK_SIZE = 512

def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)

    seq = 0

    with open("input.txt", "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                chunk = b'EOF'

            packet = make_packet(seq, chunk)

            while True:
                unsafe_send(sock, packet, SERVER_ADDR)

                try:
                    ack, _ = sock.recvfrom(1024)
                    ack_seq = struct.unpack("!B", ack)[0]

                    if ack_seq == seq:
                        print(f"ACK {ack_seq} received")
                        seq = 1 - seq
                        break

                except socket.timeout:
                    print("Timeout, resend")

            if chunk == b'EOF':
                break

    print("File sent")


if __name__ == "__main__":
    client()