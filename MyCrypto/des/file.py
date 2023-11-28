import os


def writefile(filename, data):
    with open(filename, "wb") as f:
        f.write(data)


def readfile(filename):
    result = None
    with open(filename, "rb") as f:
        result = f.read()
    return result





