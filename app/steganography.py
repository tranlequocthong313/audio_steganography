from threading import Thread


def bits_to_bytes(bits):
    tmp = "".join(map(str, bits))
    tmp = [tmp[i : i + 8] for i in range(0, len(tmp), 8)]
    tmp = [int(i, 2) for i in tmp]
    return bytes(tmp)


class Header:
    """
    This class is used to attach a header containing information of the embedded original file.
    When extracted, that information can be used to recreate the original file.
    """

    def __init__(self):
        self.STAMP = "AS"  # This is used for indentify embedded files of this app
        self.STAMP_PASS = "ASP"  # This is used for indentify embedded files of this app

    def make_header(self, hidden_bytes, filename, password=None):
        """
        This function takes in an array of data bytes and the name of the original file,
        then it returns an array of bytes with the header attached.

        Header format: STAMP + full_length + # + file_name_length + # + file_name + data_size + # + data
        Example: ASP35#8#password8#demo.txt12#Hello world!
        """
        result = b""
        if password:
            result += str(len(password.encode())).encode()
            result += "#".encode()
            result += password.encode()
        result += str(len(filename.encode())).encode()
        result += "#".encode()
        result += filename.encode()
        result += str(len(hidden_bytes)).encode()
        result += "#".encode()
        result += hidden_bytes
        full_length = str(len(result)).encode() + "#".encode()
        res = (
            (self.STAMP_PASS.encode() if password else self.STAMP.encode())
            + full_length
            + result
        )
        return res

    def validate(self, bytes):
        """
        This function is used to check if the header is valid
        """
        return "".join(map(chr, bytes[: len(self.STAMP)])) == self.STAMP

    def contains_password(self, bytes):
        """
        This function is used to check if the header contains password
        """
        return "".join(map(chr, bytes)) == self.STAMP_PASS[len(self.STAMP_PASS) - 1]

    def extract(self, embedded_bytes, password=None):
        """
        This function is used to extract the header and data bytes that has been attached to the embedded bytes
        """
        extracted_info = []
        i, j = 0, 0

        while len(extracted_info) < (3 if password else 2):
            if password and len(extracted_info) == 1:
                if password != bytes(extracted_info[0]).decode("utf-8"):
                    raise ValueError("Password must match.")
            j = i
            while embedded_bytes[j] != ord("#"):
                j += 1
            length = int("".join(map(chr, embedded_bytes[i:j])))
            extracted_info.append(embedded_bytes[j + 1 : j + 1 + length])
            i = j + 1 + length

        if password:
            return {
                "password": bytes(extracted_info[0]),
                "filename": bytes(extracted_info[1]),
                "data": bytes(extracted_info[2]),
            }
        else:
            return {
                "filename": bytes(extracted_info[0]),
                "data": bytes(extracted_info[1]),
            }


class Steganography:
    """
    This class is used to embed and extract any file into an audio file
    """

    def __init__(self) -> None:
        self.header = Header()

    def __embed(self, bits, carrier_bytes, skipped_bytes):
        """
        This function helps put bits into audio bytes
        """
        j = skipped_bytes

        for i in range(len(bits)):
            carrier_bytes[j] = (
                carrier_bytes[j] & 0xFE
            )  # reset last bit of current carrier's byte to 0
            carrier_bytes[j] = (
                carrier_bytes[j] | bits[i]
            )  # change last bit of current carrier's byte to current bit of hidden bits
            j += 1

    def embed(
        self, hidden_bytes, carrier_bytes, filename, password=None, skipped_bytes=0
    ):
        """
        This function is used to embed the bytes that need to be hidden.
        It accepts the bytes of the original file, the bytes of the carrier file
        and the number of bytes to be ignored if any.
        """
        skipped_bytes = max(skipped_bytes, 0)
        hidden_bytes = self.header.make_header(hidden_bytes, filename, password)

        if len(hidden_bytes) * 8 > len(carrier_bytes) - skipped_bytes:
            raise OverflowError("Carrier file size is too small for embedding.")

        bits = [int(bit) for byte in hidden_bytes for bit in f"{byte:08b}"]

        thread1 = Thread(
            target=self.__embed,
            args=(bits[: (len(bits) // 2)], carrier_bytes, skipped_bytes),
        )
        thread2 = Thread(
            target=self.__embed,
            args=(
                bits[(len(bits) // 2) :],
                carrier_bytes,
                skipped_bytes + len(bits) // 2,
            ),
        )

        thread1.start()
        thread2.start()
        thread1.join()
        thread2.join()

        return bytes(carrier_bytes)

    def extract(self, embedded_bytes, password=None, skipped_bytes=0):
        """
        This function is used to extract the original bytes in embedded bytes
        and the number of bytes to be ignored if any.
        """
        skipped_bytes = max(skipped_bytes, 0)
        bits = []

        index = 0
        for i in range(skipped_bytes, len(embedded_bytes)):
            if len(bits) == len(self.header.STAMP) * 8:
                if not self.header.validate(bits_to_bytes(bits)):
                    raise ValueError("This is not an embedded file.")
                else:
                    index = i
                    bits = []
                    break
            else:
                bit = (
                    embedded_bytes[i] & 0x1
                )  # extract last bit of current embedded byte's
                bits.append(bit)

        for k in range(index, len(embedded_bytes)):
            if len(bits) > 0 and len(bits) % 8 == 0:
                if self.header.contains_password(bits_to_bytes(bits)):
                    if not password:
                        raise ValueError("Require password.")
                    else:
                        index = k
                        bits = []
                        break
                else:
                    bits = []
                    break
            else:
                bit = (
                    embedded_bytes[k] & 0x1
                )  # extract last bit of current embedded byte's
                bits.append(bit)

        i, j = 0, 0
        length = 0
        for k in range(index, len(embedded_bytes)):
            bit = embedded_bytes[k] & 0x1  # extract last bit of current embedded byte's
            bits.append(bit)
            if len(bits) % 8 == 0:
                if ord(bits_to_bytes(bits[j : i + 1]).decode("utf-8")) == ord("#"):
                    length = int("".join(map(chr, bits_to_bytes(bits[0:j]))))
                    index = k + 1
                    break
                j = i + 1
            i += 1

        bits = []
        for k in range(index, index + 1 + (length * 8)):
            bit = embedded_bytes[k] & 0x1  # extract last bit of current embedded byte's
            bits.append(bit)

        return self.header.extract(bits_to_bytes(bits), password)


header_lengths = {
    "wav": 44,
}
