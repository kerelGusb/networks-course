import socket
import time

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(1.0)
server_host = "127.0.0.1"
server_port = 12345

print(f"Pinging {server_host}:{server_port}...")

rtt_list = []
lost_packets = 0

for sequence_number in range(1, 11):
    send_time = time.time()
    message = f"Ping {sequence_number} {send_time}"

    try:
        client_socket.sendto(message.encode('utf-8'), (server_host, server_port))

        response_data, _ = client_socket.recvfrom(1024)
        receive_time = time.time()

        rtt = receive_time - send_time
        rtt_list.append(round(rtt, 7))

        print(f"Reply from {server_host}: {response_data.decode('utf-8')} | RTT: {round(rtt, 7)} sec")

    except socket.timeout:
        lost_packets += 1
        print(f"Request {sequence_number}: Request timed out")

print("\nStatistics:")
print(f"Sent: 10, Received: {len(rtt_list)}, Lost: {lost_packets} ({(lost_packets/10)*100}% loss)")

if rtt_list:
    print(f"Min RTT: {min(rtt_list)} sec")
    print(f"Max RTT: {max(rtt_list)} sec")
    print(f"Avg RTT: {sum(rtt_list)/len(rtt_list)} sec")

client_socket.close()