def read_file_as_bytes(path):
    with open(path, 'rb') as file:
        bytes_data = file.read()
    return bytearray(bytes_data)


def write_bytes_to_file(byte_array, path):
    with open(path, 'wb') as file:
        file.write(byte_array)


def binary_to_byte_str(binary):
    binary = ''.join(map(str, binary))
    binary = [binary[i:i+8] for i in range(0, len(binary), 8)]
    binary = [int(i, 2) for i in binary]
    return ''.join(chr(i) for i in binary)


def binary_to_byte(binary, start=0, end=0):
    binary = ''.join(map(str, binary))
    binary = [binary[i:i+8] for i in range(start, end, 8)]
    return [int(i, 2) for i in binary]


def bytes_to_binary(byte_array):
    return [int(bit) for byte in byte_array for bit in f'{byte:08b}']
