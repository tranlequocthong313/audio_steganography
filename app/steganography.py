def bits_to_bytes(bits):
    tmp = ''.join(map(str, bits))
    tmp = [tmp[i:i+8] for i in range(0, len(tmp), 8)]
    tmp = [int(i, 2) for i in tmp]
    return bytes(tmp)


class Header:
    '''
    This class is used to attach a header containing information of the embedded original file. 
    When extracted, that information can be used to recreate the original file. 
    '''

    def __init__(self):
        self.STAMP = 'AS' # This is used for indentify embedded files of this app


    def make_header(self, hidden_bytes, filename):
        '''
        This function takes in an array of data bytes and the name of the original file, 
        then it returns an array of bytes with the header attached. 

        Header format: STAMP + file_name_length + # + file_name + data_size + # + data
        Example: AS8#demo.txt12#Hello world!
        '''
        result = self.STAMP.encode()
        result += str(len(filename)).encode() 
        result += "#".encode()
        result += filename.encode() 
        result += str(len(hidden_bytes)).encode() 
        result += "#".encode()
        result += hidden_bytes
        return result


    def validate(self, bytes):
        '''
        This function is used to check if the header is valid 
        '''
        return ''.join(map(chr, bytes[:len(self.STAMP)])) == self.STAMP
        

    def extract(self, embedded_bytes):
        '''
        This function is used to extract the header and data bytes that has been attached to the embedded bytes 
        '''
        if self.validate(embedded_bytes) == False:
            raise ValueError('Not an embedded file.')

        embedded_bytes = embedded_bytes[len(self.STAMP):] # skip stamp bytes
        extracted_info = []
        i, j = 0, 0
        
        while len(extracted_info) < 2:
            j = i
            while embedded_bytes[j] != ord('#'):
                j += 1
            length = int(''.join(map(chr, embedded_bytes[i:j])))
            extracted_info.append(embedded_bytes[j+1 : j+1+length]) 
            i = j + 1 + length
        
        return {
            'filename': bytes(extracted_info[0]),
            'data': bytes(extracted_info[1]),
        }


class Steganography:
    '''
    This class is used to embed and extract any file into an audio file 
    '''
    def __init__(self) -> None:
        self.header = Header()


    def embed(self, hidden_bytes, carrier_bytes, filename, skipped_bytes=0):
        '''
        This function is used to embed the bytes that need to be hidden. 
        It accepts the bytes of the original file, the bytes of the carrier file 
        and the number of bytes to be ignored if any.
        '''
        skipped_bytes = max(skipped_bytes, 0)
        hidden_bytes = self.header.make_header(hidden_bytes, filename)

        if (len(hidden_bytes) * 8 > len(carrier_bytes) - skipped_bytes):
            raise OverflowError('Not enough size to embed.')

        bits = [int(bit) for byte in hidden_bytes for bit in f'{byte:08b}']
        j = skipped_bytes

        for i in range(len(bits)):
            carrier_bytes[j] = carrier_bytes[j] & 0xFE # reset last bit of current carrier's byte to 0
            carrier_bytes[j] = carrier_bytes[j] | bits[i] # change last bit of current carrier's byte to current bit of hidden bits
            j += 1

        return bytes(carrier_bytes)


    def extract(self, embedded_bytes, skipped_bytes=0):
        '''
        This function is used to extract the original bytes in embedded bytes
        and the number of bytes to be ignored if any.
        '''
        skipped_bytes = max(skipped_bytes, 0)
        bits = []

        for i in range(skipped_bytes, len(embedded_bytes)):
            bit = embedded_bytes[i] & 0x1 # extract last bit of current embedded byte's
            bits.append(bit)

        return self.header.extract(bits_to_bytes(bits))


header_lengths = {
    'wav': 44,
}


# if __name__ == '__main__':
#     hidden_path = 'app/img.jpg'
#     hidden_filename = 'img.jpg'
#     carrier_filename = 'song2.wav'
#     file_format = 'wav'
#     embedded_filename = f'embedded.{file_format}'

#     with open(hidden_path, 'rb') as f:
#         hidden_bytes = bytearray(f.read())
#     with open(carrier_filename, 'rb') as f:
#         carrier_bytes = bytearray(f.read())
    
#     steganography = Steganography()
#     embedded_bytes = steganography.embed(hidden_bytes, carrier_bytes, hidden_filename, skipped_bytes=header_lengths[file_format]+1)

#     with open(embedded_filename, 'wb') as f:
#         f.write(embedded_bytes)

#     with open(embedded_filename, 'rb') as f:
#         embedded_bytes = bytearray(f.read())
#     info = steganography.extract(embedded_bytes, header_lengths[file_format] + 1)
#     with open(info['filename'], 'wb') as f:
#         f.write(info['data'])
