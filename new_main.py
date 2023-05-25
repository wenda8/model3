import json
from new_bulid_index import build_index
from new_compress import elias_coding_gamma, elias_coding_delta, elias_decoding_gamma, elias_decoding_delta, elias_delta_decode
import time
import pickle
from bitarray import bitarray

with open('config.json', 'r', encoding='utf-8') as cf:
    config = json.load(cf)

folder_path = config['folder_path']
csv_file_name = config['csv_file_name']
file_index = config['file_index']
inverted_index = config['inverted_index']
key_word = config['key_word'].lower()
elias_gamma = config['elias_gamma']
elias_delta = config['elias_delta']
length_gamma_id = config['length_gamma_id']
length_delta_id = config['length_delta_id']
length_inverted = config['length_inverted']
length_elias_gamma = config['length_elias_gamma']
length_elias_delta = config['length_elias_delta']

build_index(csv_file_name, file_index, folder_path, inverted_index)

with open('inverted_index.json', 'r', encoding='utf-8') as inverted_jsonfile:
    inverted_index_search = json.load(inverted_jsonfile)


def search_key_words(key_word):
    with open('file_index.json', 'r', encoding='utf-8') as file_jsonfile:
        file_index_search = json.load(file_jsonfile)
    with open('gamma_index.pkl', 'rb') as gammafile:
        gamma_index = pickle.load(gammafile)
    with open('delta_index.pkl', 'rb') as deltafile:
        delta_index = pickle.load(deltafile)

    n = 0
    for inverted_key, inverted_value in inverted_index_search.items():
        if inverted_key == key_word:
            txt_id = inverted_value
            info_key_word = {}
            for i in txt_id:
                for index, name in file_index_search.items():
                    if int(i) == int(index):
                        info_key_word[index] = name
                        n += 1

    for gamma_key, gamma_value in gamma_index.items():
        if gamma_key == key_word:
            txt_gamma_id = gamma_value

    for delta_key, delta_value in delta_index.items():
        if delta_key == key_word:
            txt_delta_id = delta_value

    print(f"Search word is:{key_word}\nnumber of key words: {n}\nID and Filename is {info_key_word}\nID in Gamma index is {txt_gamma_id}\nID in Delta index is {txt_delta_id}")


def encoding_elias_gamma(elias_gamma: dict, length_gamma_id: dict): 
    for inverted_key, inverted_value in inverted_index_search.items(): # traverse in inverted index
        elias_gamma[inverted_key] = [] 
        gamma_bit = []
        length_gamma_id[inverted_key] = []
        for single_id in inverted_value:  # traverse every element in list
            gamma_value = elias_coding_gamma(single_id)
            gamma_bit.append(gamma_value)
            length_gamma_id[inverted_key].append(len(gamma_value))
            length_inverted.append(single_id)

        gamma_bit = bitarray(''.join(gamma_bit))   # use bitarray, which take str to bit and then 8bit = 1byte
        elias_gamma[inverted_key] = gamma_bit.tobytes()


    total_inverted_bytes = sum(len(str(num)) for num in length_inverted) * 4
    total_gamma_bytes = sum(len(str(num)) for num in elias_gamma.values())
    # print(total_inverted_bytes)
    # print(total_gamma_bytes)


    with open('gamma_index.pkl', 'wb') as gamma_file:
        pickle.dump(elias_gamma, gamma_file)
    with open('length_gamma.json', 'w', encoding='utf-8') as length_gamma_file: # easy to read
        json.dump(length_gamma_id, length_gamma_file, ensure_ascii=False)

    return total_gamma_bytes, total_inverted_bytes
    

def encoding_elias_delta(elias_delta: dict, length_delta_id: dict): # the same as elias gamma
    for inverted_key, inverted_value in inverted_index_search.items():
        elias_delta[inverted_key] = []
        delta_bit = []
        length_delta_id[inverted_key] = []
        for single_id in inverted_value:
            delta_value = elias_coding_delta(single_id)
            delta_bit.append(delta_value)
            length_delta_id[inverted_key].append(len(delta_value))
            length_inverted.append(single_id)
        
        delta_bit = bitarray(''.join(delta_bit))
        elias_delta[inverted_key] = delta_bit.tobytes()

    total_inverted_bytes = sum(len(str(num)) for num in length_inverted) * 4
    total_delta_bytes = sum(len(str(num)) for num in elias_delta.values())
    # print(total_inverted_bytes)
    # print(total_delta_bytes)

    with open('delta_index.pkl', 'wb') as delta_file:
        pickle.dump(elias_delta, delta_file)
    with open('length_delta.json', 'w') as length_delta_file:
        json.dump(length_delta_id, length_delta_file)

    return total_delta_bytes
    

def decoding_elias_gamma():
    with open('gamma_index.pkl', 'rb') as decode_gamma:
        pre_gamma_index = pickle.load(decode_gamma)
    with open('length_gamma.json', 'r', encoding='utf-8') as length_file:
        length_dict = json.load(length_file)

    decode_gamma_str = {}
    for pre_key, pre_value in pre_gamma_index.items(): # let bitarray = str
        gamma_str = bitarray()
        gamma_str.frombytes(pre_value)
        decode_gamma_str[pre_key] = gamma_str.to01()

    def split_gamma_coding(length_dict, decode_gamma_str):
        decode_gamma_code = {}
        for key in length_dict.keys():  # decode_gamma_str is like '0001110101010101'
            lengths = length_dict[key]
            encode_str = decode_gamma_str[key]
            split_value = []
            start = 0
            for length in lengths:
                split_value.append(encode_str[start:start + length])
                start += length
            decode_gamma_code[key] = split_value

        return decode_gamma_code

    decode_gamma_code = split_gamma_coding(length_dict, decode_gamma_str)
    
    degamma_inverted = {}

    for gamma_key, gamma_value in decode_gamma_code.items():
        degamma_inverted[gamma_key] = []
        for single_value in gamma_value:
            single_value = elias_decoding_gamma(single_value)
            degamma_inverted[gamma_key].append(single_value)

    # print(degamma_inverted)
    return degamma_inverted
    

def decoding_elias_delta():  # the same as elias_gamma
    with open('delta_index.pkl', 'rb') as decode_delta:
        pre_delta_index = pickle.load(decode_delta)
    with open('length_delta.json', 'r', encoding='utf-8') as length_file:
        length_dict = json.load(length_file)

    decode_delta_str = {}
    for pre_key, pre_value in pre_delta_index.items():
        delta_str = bitarray()
        delta_str.frombytes(pre_value)
        decode_delta_str[pre_key] = delta_str.to01()

    def split_delta_coding(length_dict, decode_delta_str):
        decode_delta_code = {}
        for key in length_dict.keys():
            lengths = length_dict[key]
            encode_str = decode_delta_str[key]
            split_value = []
            start = 0
            for length in lengths:
                split_value.append(encode_str[start:start + length])
                start += length
            decode_delta_code[key] = split_value

        return decode_delta_code

    decode_delta_code = split_delta_coding(length_dict, decode_delta_str)
    
    dedelta_inverted = {}

    for delta_key, delta_value in decode_delta_code.items():
        dedelta_inverted[delta_key] = []
        for single_value in delta_value:
            single_value = elias_decoding_delta(elias_delta_decode, single_value)
            dedelta_inverted[delta_key].append(single_value)

    # print(dedelta_inverted)
    return dedelta_inverted




start_time = time.time()
total_gamma_bytes, total_inverted_bytes = encoding_elias_gamma(elias_gamma, length_gamma_id)

total_delta_bytes = encoding_elias_delta(elias_delta, length_delta_id)

decoding_elias_gamma()
decoding_elias_delta()
search_key_words(key_word)

end_time = time.time()
run_time = end_time - start_time
print(f"The time of this funciton is {run_time}s")
print(f"The bytes of whole inverted index is {total_inverted_bytes}\nThe bytes of whole Gamma index is {total_gamma_bytes}\nThe bytes of whole Delta index is {total_delta_bytes}")
