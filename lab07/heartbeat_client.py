import socket
import time
import sys
import random

host = '127.0.0.1'
port = 12346
interval = 1

client_id = f"Client-{random.randint(1000, 9999)}"
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print(f"Client '{client_id}' started")
seq = 0

try:
    while True:
        seq += 1
        msg = f"HEARTBEAT {seq} {time.time()}"
        sock.sendto(msg.encode('utf-8'), (host, port))
        print(f"Sent seq={seq}")
        time.sleep(interval)

except Exception as e:
    print(f"Client '{client_id}' stopped. Error: {e}")
    sock.close()