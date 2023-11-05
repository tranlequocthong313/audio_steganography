from utils import binary_to_byte_str, bytes_to_binary, binary_to_byte


class AudioSteganography:
    STAMP = 'AS'

    def embed_data(self, hidden_bytes=[], carrier_bytes=[], header={}):
        file_name_length_bytes = str(len(header['file_name'])).encode()
        file_name_bytes = header['file_name'].encode()
        data_length_bytes = str(header['size']).encode()
        hidden_bytes = self.STAMP.encode() + file_name_length_bytes + "#".encode() + file_name_bytes + data_length_bytes + '#'.encode() + hidden_bytes
        bits = bytes_to_binary(hidden_bytes)

        j = 45
        for i in range(len(bits)):
            carrier_bytes[j] = carrier_bytes[j] & 254  # use last bit of byte
            carrier_bytes[j] = carrier_bytes[j] | bits[i]
            j += 1

        return bytes(carrier_bytes)

    def extract_data(self, carrier_bytes=[]):
        extracted = []

        for i in range(45, len(carrier_bytes)):
            bit = carrier_bytes[i] & 1
            extracted.append(bit)

        stamp_bytes = extracted[:len(self.STAMP) * 8]
        sign = binary_to_byte_str(stamp_bytes)

        if sign == self.STAMP:
            print('OK')
        else:
            print('NOT OK')

        tmp = binary_to_byte_str(extracted)
        tmp = tmp[2:]
        res, i = [], 0
        lengths = []
        j = 0
        header = ''
        while len(res) < 2:
            j = i
            while tmp[j] != '#':
                j += 1
                header += tmp[j]
            length = int(tmp[i:j])
            lengths.append(length)
            res.append(tmp[j+1:j+1+length])
            i = j + 1 + length

        binary = ''.join(map(str, extracted))
        binary = [binary[i:i+8] for i in range((j+3)*8, lengths[1]*8 + (j+3)*8, 8)]
        binary = [int(i, 2) for i in binary]

        start = (j+3) * 8
        end = lengths[1]*8 + (j+3)*8
        result = binary_to_byte(extracted, start, end)

        return {
            'bytes': bytes(result),
            'file_name': res[0]
        }
