import socket
import fcntl
import struct

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    ip = s.getsockname()[0]
    s.close()
    print(f"IP-address: {ip}")

    iface = input("Input interface name: ")

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    netmask = socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x891b,
        struct.pack('256s', iface.encode())
    )[20:24])
    s.close()
    print(f"Netmask: {netmask}")

if __name__ == "__main__":
    main()