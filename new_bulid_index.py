import csv
from new_clean import clean_word
import os 
import time 
import json
import pickle


def divide_to_txt(csv_file_name, file_index, index, folder_path):
    os.makedirs(folder_path, exist_ok=True)
    with open(csv_file_name, 'r', encoding='utf-8') as csv_file:
        data_csv = csv.reader(csv_file)
        header = next(data_csv)

        for row in data_csv:
            if len(row) >= 9:
                filename = f"{row[0]}_{row[8]}.txt"
                file_path = os.path.join(folder_path, filename) 
                with open(file_path, 'w', encoding='utf-8') as txt_file:
                    txt_file.write(','.join(header) + '\n')
                    txt_file.write(','.join(row))
                    file_index[index] = filename
                    index += 1
            else:
                print(f"Error:{row}")

    return file_index, index

    
def build_inverted_index(file_index, inverted_index, folder_path):
    for index, filename in file_index.items():
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as single_file:
            text = single_file.read()
            set_words = set(clean_word(text))
            for w in set_words:
                if w not in inverted_index:
                    inverted_index[w] = [index]
                else:
                    inverted_index[w].append(index)
    return inverted_index


def save_index(file_index, inverted_index):
    with open('file_index.json', 'w', encoding='utf-8') as file_save:
        json.dump(file_index, file_save)
    with open('inverted_index.json', 'w', encoding='utf-8') as inverted_save:
        json.dump(inverted_index, inverted_save, ensure_ascii=False)
    # # if wanna see russian words in json
    # with open('inverted_index.json', 'w', encoding='utf-8') as inverted_save:
    #     json.dump(inverted_index, inverted_save, ensure_ascii=False)
    with open('file_index.pkl', 'wb') as file_save:
        pickle.dump(file_index, file_save)
    with open('inverted_index.pkl', 'wb') as inverted_save:
        pickle.dump(inverted_index, inverted_save)

def build_index(csv_file_name, file_index, folder_path, inverted_index):
    file_index, index = divide_to_txt(csv_file_name, file_index, 1, folder_path)
    inverted_index = build_inverted_index(file_index, inverted_index, folder_path)
    save_index(file_index, inverted_index)





# print(inverted_index)
# print(f"{run_time}秒")
