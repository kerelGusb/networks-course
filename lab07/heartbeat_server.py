import socket
import time
import threading

host = '127.0.0.1'
port = 12346
timeout = 5

clients = {}
lock = threading.Lock()

def monitor_clients():
    while True:
        time.sleep(1)
        current_time = time.time()
        with lock:
            to_remove = []
            for addr, data in clients.items():
                if data['last_time'] > 0 and current_time - data['last_time'] > timeout:
                    print(f"[WARNING] Client {addr} inactive for {timeout}s")
                    print(f"          Last seq: {data['last_seq']}, Lost: {data['lost']}")
                    to_remove.append(addr)
            for addr in to_remove:
                del clients[addr]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((host, port))
print(f"Server started on {host}:{port}")

threading.Thread(target=monitor_clients, daemon=True).start()

while True:
    data, addr = server_socket.recvfrom(1024)
    msg = data.decode('utf-8')
    current_time = time.time()
    
    parts = msg.split()
    if len(parts) < 3 or parts[0] != "HEARTBEAT":
        continue
    
    seq = int(parts[1])
    timestamp = float(parts[2])
    
    with lock:
        if addr not in clients:
            clients[addr] = {'last_seq': 0, 'last_time': 0, 'lost': 0}
            print(f"[NEW] Client {addr}")
        
        c = clients[addr]
        if seq > c['last_seq'] + 1:
            lost = seq - c['last_seq'] - 1
            c['lost'] += lost
            print(f"[LOSS] {addr}: {lost} packets (seq {c['last_seq']+1}-{seq-1})")
        
        diff = current_time - timestamp
        print(f"[RECV] {addr[0]}:{addr[1]} seq={seq} diff={diff:.6f}s lost={c['lost']}")
        
        c['last_seq'] = seq
        c['last_time'] = current_time