import os


def write(filename, data):
    with open(filename, "wb") as f:
        f.write(data)


def read(filename):
    result = None
    with open(filename, "rb") as f:
        result = bytearray(f.read())
    return result
