
def elias_coding_gamma(n_10):
    if n_10 <= 0:
        print("ID must be positive integer")
    else:
        gamma_binary = bin(n_10)[2:]
        gamma_unary = (len(gamma_binary) - 1) * '0'
        gamma_code = gamma_unary + gamma_binary
    return gamma_code

def elias_decoding_gamma(n_2):
    if n_2 == '1':
        return 1
    else:
        index_unary, index_binary = n_2.split('0', 1)
        return int(index_binary, 2)

def elias_coding_delta(n_10):
    if n_10 <= 0:
        print("ID must be positive integer")
    else:
        delta_binary = bin(n_10)[2:]
        length = len(delta_binary)
        delta_gamma = elias_coding_gamma(length)
        no_highest_delta_binary = delta_binary[1:]
        delta_code = delta_gamma + no_highest_delta_binary
   
    return delta_code
    
print(elias_coding_delta(10))
class BitReader:
    def __init__(self, source):
        self.source = list(source)
        self.index = 0

    def has_left(self):
        return self.index < len(self.source)

    def input_bit(self):
        if self.has_left():
            bit = self.source[self.index]
            self.index += 1
            return bit
        else:
            raise Exception('No bits left to read')

class IntWriter:
    def __init__(self):
        self.data = []

    def put_int(self, num):
        self.data.append(num)

    def get_data(self):
        return self.data

def elias_delta_decode(source):
    bitreader = BitReader(source)
    intwriter = IntWriter()
    while bitreader.has_left():
        lengthOfLen = 0
        while bitreader.has_left() and not bitreader.input_bit():
            lengthOfLen += 1
        len = 1
        for _ in range(lengthOfLen):
            len <<= 1
            if bitreader.has_left() and bitreader.input_bit():
                len |= 1
        num = 1
        for _ in range(len-1):
            num <<= 1
            if bitreader.has_left() and bitreader.input_bit():
                num |= 1
        intwriter.put_int(num)
    return int(intwriter.get_data()[0])

def elias_decoding_delta(elias_delta_decode, delta_coding):
    binary_str = delta_coding
    binary_list = [int(bit) for bit in binary_str]
    decode_delta = elias_delta_decode(binary_list)
    # print(decode_delta)
    return decode_delta


delta_coding = "001010001"
elias_decoding_delta(elias_delta_decode, delta_coding)
# print(elias_coding_gamma(0))
# print(elias_decoding_gamma(n_2))
# print(elias_coding_delta(n_10))