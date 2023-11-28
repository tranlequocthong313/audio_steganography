class DES_base:
    
    def __init__(self):
        pass
    
    @staticmethod
    def get_bit(data, digit):
        ''' return the i-th bit of data '''
        return (data >> digit) & 1
    
    @staticmethod
    def cyclic_lshift(data, length, digit):
        for i in range(digit):
            data = ((data << 1) & ((1 << length) - 1)) ^ (data >> (length - 1))
        return data
    
    @staticmethod
    def split_bit(data, length, time):
        ''' split data to tuple '''
        assert length % time == 0
        split_len = length // time
        results = list()
        for t in range(time):
            results.insert(0, data & ((1 << split_len) - 1))
            data >>= split_len
        return results
    @staticmethod
    def split_bytes(input_bytes, chunk_size):
        # Khởi tạo biến để lưu trữ chuỗi con
        result_str = b""

        # Chạy vòng lặp while để cắt chuỗi cho đến khi hết
        i = 0
        while i < len(input_bytes):
            # Cắt một chuỗi con với kích thước chunk và thêm vào biến kết quả
            result_str = input_bytes[i:i + chunk_size]

            # Tăng chỉ số để di chuyển đến phần tử tiếp theo
            i += chunk_size

        return result_str

    @staticmethod
    def merge_bit(data, length):
        ''' merge data tuple '''
        result = 0
        for d in data:
            result <<= length
            result ^= d
        return result

    @staticmethod
    def verify_key(raw_key):
        ''' verify the key '''
        for i in range(8):
            presult = 1 # ODD
            for j in range(8):
                sig = DES_base.get_bit(raw_key, 8*(7-i)+(7-j))
                if j == 7:
                    if sig != presult:
                        return False
                else:
                    presult ^= sig
        return True
    
    @staticmethod
    def permutation(data, table, length):
        ''' do permutation based on table '''
        result = 0
        for t in table:
            result <<= 1
            result ^= DES_base.get_bit(data, length-t)
        return result
