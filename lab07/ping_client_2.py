import socket
import time
import statistics

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)

server_host = "127.0.0.1"
server_ip = "127.0.0.1"
server_port = 12345

print(f"PING {server_host} ({server_ip}) 56(84) bytes of data.")

rtt_list = []
lost_packets = 0
sequence_number = 1
start_time = time.time()

try:
    while sequence_number <= 10:
        send_time = time.time()
        message = f"PING {sequence_number} {send_time}"

        try:
            client_socket.sendto(message.encode('utf-8'), (server_host, server_port))
            response_data, _ = client_socket.recvfrom(1024)
            receive_time = time.time()

            rtt = (receive_time - send_time) * 1000
            rtt_list.append(rtt)

            print(f"64 bytes from {server_host} ({server_ip}): icmp_seq={sequence_number} ttl=64 time={rtt:.3f} ms")

        except socket.timeout:
            lost_packets += 1

        sequence_number += 1
        time.sleep(1)

except Exception as e:
    print(f"Error: {e}")

total_time_ms = (time.time() - start_time) * 1000

print(f"--- {server_host} ping statistics ---")
total_sent = sequence_number - 1
total_received = len(rtt_list)
loss_percentage = (lost_packets / total_sent) * 100 if total_sent > 0 else 0

print(f"{total_sent} packets transmitted, {total_received} received, {loss_percentage:.0f}% packet loss, time {total_time_ms:.0f}ms")

if rtt_list:
    min_rtt = min(rtt_list)
    avg_rtt = statistics.mean(rtt_list)
    max_rtt = max(rtt_list)
    if len(rtt_list) > 1:
        mdev = statistics.stdev(rtt_list)
    else:
        mdev = 0

    print(f"rtt min/avg/max/mdev = {min_rtt:.3f}/{avg_rtt:.3f}/{max_rtt:.3f}/{mdev:.3f} ms")

client_socket.close()