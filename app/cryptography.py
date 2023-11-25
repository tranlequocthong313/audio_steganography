class Cryptography:
    def encrypt(self, message, password):
        for i, c in enumerate(message):
            message[i] = (c + password[i % len(password)]) % 0x100
        return bytes(message)

    def decrypt(self, message, password):
        for i, c in enumerate(message):
            message[i] = ((c - password[i % len(password)]) + 0x100) % 0x100
        return bytes(message)
