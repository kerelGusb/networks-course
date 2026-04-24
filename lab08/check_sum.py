def compute_checksum(data):
    if len(data) % 2 != 0:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        checksum += data[i] << 8
        checksum += data[i + 1]
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return ~checksum & 0xFFFF


def verify_checksum(data, checksum):
    if len(data) % 2 != 0:
        data += b'\x00'

    total = checksum
    for i in range(0, len(data), 2):
        total += data[i] << 8
        total += data[i + 1]
        total = (total & 0xFFFF) + (total >> 16)

    return total == 0xFFFF


def run_tests():
    data = b'hello'
    checksum = compute_checksum(data)
    print("Test 1 (correct):", verify_checksum(data, checksum))

    corrupted = bytearray(data)
    corrupted[0] ^= 0x01
    print("Test 2 (corrupted):", verify_checksum(corrupted, checksum))

    data = b''
    checksum = compute_checksum(data)
    print("Test 3 (empty):", verify_checksum(data, checksum))


if __name__ == "__main__":
    run_tests()