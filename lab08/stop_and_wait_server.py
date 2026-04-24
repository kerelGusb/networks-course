import socket
from stop_and_wait_utils import *

SERVER_ADDR = ("localhost", 9999)


def server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(SERVER_ADDR)

    expected_seq = 0
    received_data = b''

    print("Server started")

    while True:
        packet, addr = sock.recvfrom(2048)

        seq, data, valid = parse_packet(packet)

        if not valid:
            print("Corrupted packet")
            continue

        print(f"Received seq={seq}")

        if seq == expected_seq:
            if data == b'EOF':
                print("EOF received")

                with open("received.txt", "wb") as f:
                    f.write(received_data)

                print("File saved")

                received_data = b''
                expected_seq = 0

            else:
                received_data += data
                expected_seq = 1 - expected_seq
        else:
            print("Duplicate packet")

        ack = struct.pack("!B", seq)
        unsafe_send(sock, ack, addr)

    print("File received")


if __name__ == "__main__":
    server()