import pytest

from steganography import Steganography


def test_embed_success():
    hidden_bytes = "Hello world!".encode()
    carrier_bytes = list(("A"*300).encode())    
    filename = "test.txt"
    skipped_bytes = 10
    steganography = Steganography()

    actual = steganography.embed(hidden_bytes, carrier_bytes, filename, skipped_bytes)

    assert actual == b'AAAAAAAAAA@A@@@@@A@A@A@@AA@@AAA@@@@@A@@@AA@AAA@A@@@AA@@A@A@AAA@@AA@AAA@A@@@@A@AAA@@AAA@A@@@AAAA@@@@AAA@A@@@@AA@@@A@@AA@@A@@@A@@@AA@A@@A@@@@AA@@A@A@AA@AA@@@AA@AA@@@AA@AAAA@@A@@@@@@AAA@AAA@AA@AAAA@AAA@@A@@AA@AA@@@AA@@A@@@@A@@@@AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'


def test_embed_fail():
    hidden_bytes = "Hello world!".encode()
    carrier_bytes = list(("A"*100).encode())    
    filename = "test.txt"
    skipped_bytes = 10
    steganography = Steganography()

    with pytest.raises(OverflowError):
        steganography.embed(hidden_bytes, carrier_bytes, filename, skipped_bytes)


def test_full_process():
    hidden_bytes = "Hello world!".encode()
    filename = "test.txt"
    skipped_bytes = 10
    steganography = Steganography()
    embedded_bytes = b'AAAAAAAAAA@A@@@@@A@A@A@@AA@@AAA@@@@@A@@@AA@AAA@A@@@AA@@A@A@AAA@@AA@AAA@A@@@@A@AAA@@AAA@A@@@AAAA@@@@AAA@A@@@@AA@@@A@@AA@@A@@@A@@@AA@A@@A@@@@AA@@A@A@AA@AA@@@AA@AA@@@AA@AAAA@@A@@@@@@AAA@AAA@AA@AAAA@AAA@@A@@AA@AA@@@AA@@A@@@@A@@@@AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'

    actual = steganography.extract(embedded_bytes, skipped_bytes)

    assert actual['filename'] == filename.encode()
    assert actual['data'] == hidden_bytes


def test_full_process():
    hidden_bytes = "Hello world!".encode()
    carrier_bytes = list(("A"*300).encode())    
    filename = "test.txt"
    skipped_bytes = 10
    steganography = Steganography()

    embedded_bytes = steganography.embed(hidden_bytes, carrier_bytes, filename, skipped_bytes)
    actual = steganography.extract(embedded_bytes, skipped_bytes)

    assert actual['filename'] == filename.encode()
    assert actual['data'] == hidden_bytes
