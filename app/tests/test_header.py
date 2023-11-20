import pytest

from steganography import Header


def test_make_header():
    hidden_bytes = 'Hello world!'.encode()
    filename = "test.txt"
    header = Header()
    expected = header.STAMP.encode() + str(len(filename)).encode() + '#'.encode() + filename.encode() + str(len(hidden_bytes)).encode() + '#'.encode() + hidden_bytes

    actual = header.make_header(hidden_bytes, filename)

    assert expected == actual


def test_validate_true():
    bytes = [65, 83]
    header = Header()

    actual = header.validate(bytes)

    assert actual == True


def test_validate_false():
    bytes = [66, 84]
    header = Header()

    actual = header.validate(bytes)

    assert actual == False


def test_extract_success():
    hidden_bytes = 'Hello world!'
    filename = "test.txt"
    header = Header()
    
    embedded_bytes = [
        65, 83, 56, 35, 116, 101, 115, 116, 
        46, 116, 120, 116, 49, 50, 35, 72, 
        101, 108, 108, 111, 32, 119, 111, 
        114, 108, 100, 33
    ] # AS8#test.txt12#Hello world!

    acutal = header.extract(embedded_bytes)

    assert acutal['filename'].decode('utf-8') == filename
    assert acutal['data'].decode('utf-8') == hidden_bytes
    

def test_extract_fail():
    header = Header()
    
    embedded_bytes = [
        67, 83, 56, 35, 116, 101, 115, 116, 
        46, 116, 120, 116, 49, 50, 35, 72, 
        101, 108, 108, 111, 32, 119, 111, 
        114, 108, 100, 33
    ] # CS8#test.txt12#Hello world!

    with pytest.raises(ValueError):
        header.extract(embedded_bytes)

    
    
