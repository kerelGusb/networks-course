import socket
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ip")
    parser.add_argument("port_from", type=int)
    parser.add_argument("port_to", type=int)
    args = parser.parse_args()

    print(f"Open ports on {args.ip} [{args.port_from}-{args.port_to}]: ")

    for port in range(args.port_from, args.port_to + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.1)
        if s.connect_ex((args.ip, port)) != 0:
            print(port)
        s.close()


if __name__ == "__main__":
    main()