import struct
import random
from check_sum import *

LOSS_PROBABILITY = 0.3

def make_packet(seq, data):
    header = struct.pack("!B", seq)
    checksum = compute_checksum(header + data)
    return struct.pack("!BH", seq, checksum) + data


def parse_packet(packet):
    seq, checksum = struct.unpack("!BH", packet[:3])
    data = packet[3:]

    calc_checksum = compute_checksum(struct.pack("!B", seq) + data)

    return seq, data, checksum == calc_checksum


def unsafe_send(sock, data, addr):
    if random.random() > LOSS_PROBABILITY:
        sock.sendto(data, addr)
    else:
        print("Packet lost")