import hashlib
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad


def generate_des_key_from_string(input_string):
    # Băm chuỗi đầu vào để có một giá trị ngẫu nhiên và không đoán được
    hashed_value = hashlib.sha256(input_string.encode('utf-8')).digest()

    # Chọn 8 byte đầu tiên từ giá trị băm để làm khóa DES
    des_key = hashed_value[:8]

    return des_key

def des_encrypt(input_bytes, des_key):
    # Chuyển đổi key từ bytes sang DES key object
    des_cipher = DES.new(des_key, DES.MODE_ECB)

    # Mã hóa chuỗi bytes và thêm padding
    ciphertext = des_cipher.encrypt(pad(input_bytes, DES.block_size))

    return ciphertext

def des_decrypt(ciphertext, des_key):
    # Chuyển đổi key từ bytes sang DES key object
    des_cipher = DES.new(des_key, DES.MODE_ECB)

    # Giải mã chuỗi bytes và loại bỏ padding
    decrypted_bytes = unpad(des_cipher.decrypt(ciphertext), DES.block_size)

    return decrypted_bytes

if __name__ == '__main__':

    with open('../testdata/filetest.docx', 'rb') as file:
        input_bytes = file.read()

    # Chuỗi đầu vào
    input_string = "huynhduydong"

    # Sinh khóa DES từ chuỗi
    des_key = generate_des_key_from_string(input_string)
    print(des_key)
    # Mã hóa
    encrypted_bytes = des_encrypt(input_bytes, des_key)
    print("Encrypted:", encrypted_bytes)
    # Giải mã
    decrypted_bytes = des_decrypt(encrypted_bytes, des_key)

    print("Decrypted:", decrypted_bytes)
