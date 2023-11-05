from steganography import AudioSteganography
from utils import read_file_as_bytes, write_bytes_to_file

import os
all_files = [f for f in os.listdir('test_files')]

for f in all_files:
    try:
        data_file = f'test_files/{f}'
        carrier_file = 'sample-file-1.wav'

        hidden_data_bytes = read_file_as_bytes(data_file)
        carrier_data_bytes = read_file_as_bytes(carrier_file)

        stega = AudioSteganography()
        embedded_bytes = stega.embed_data(hidden_bytes=hidden_data_bytes, carrier_bytes=carrier_data_bytes, header={'file_name': f, 'size': len(hidden_data_bytes)})
        write_bytes_to_file(byte_array=embedded_bytes, path='embeded.wav')

        result_bytes = read_file_as_bytes(path='embeded.wav')
        result = stega.extract_data(carrier_bytes=result_bytes)

        write_bytes_to_file(byte_array=result['bytes'], path=f"output_files/{result['file_name']}")
    except Exception as e:
        print(e)
        continue
    
