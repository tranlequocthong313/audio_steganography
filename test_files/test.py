from steganography import AudioSteganography
from utils import read_file_as_bytes, write_bytes_to_file


data_file = 'test_files/mobi2.mobi'
carrier_file = 'test_files/sample-file-1.wav'

hidden_data_bytes = read_file_as_bytes(data_file)
carrier_data_bytes = read_file_as_bytes(carrier_file)

stega = AudioSteganography()
embedded_bytes = stega.embed_data(hidden_bytes=hidden_data_bytes, carrier_bytes=carrier_data_bytes, header={'file_name': data_file, 'size': len(hidden_data_bytes)})
write_bytes_to_file(byte_array=embedded_bytes, path='output_files/res.wav')

result_bytes = read_file_as_bytes(path='output_files/res.wav')
result = stega.extract_data(carrier_bytes=result_bytes)

write_bytes_to_file(byte_array=result['bytes'], path=f"output_files/{result['file_name']}")
