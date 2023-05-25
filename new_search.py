import json

def search_data(key_word):
    with open('inverted_index.json', 'r') as jsonfile:
        inverted_index_search = json.load(jsonfile)

    for key, value in inverted_index_search.items():
        if key == key_word:
            return value
