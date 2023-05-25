import unittest
from new_bulid_index import build_index
from new_compress import elias_coding_gamma, elias_coding_delta, elias_decoding_gamma, elias_decoding_delta, elias_delta_decode, encoding_elias_gamma
from new_search import search_data

class TestSearchData(unittest.TestCase):
    def test_search_data_existing_key(self):
        # Test searching for an existing keyword
        keyword = "apple"
        expected_result = ["file1.txt", "file3.txt"]
        result = search_data(keyword)
        self.assertEqual(result, expected_result)

    def test_search_data_nonexistent_key(self):
        # Test searching for a non-existent keyword
        keyword = "banana"
        expected_result = None
        result = search_data(keyword)
        self.assertEqual(result, expected_result)

class TestEncodingDecoding(unittest.TestCase):
    def test_elias_decoding_gamma(self):
        # Test elias_decoding_gamma function
        self.assertEqual(elias_decoding_gamma('00100'), 4)

    def test_elias_decoding_delta(self):
        # Test elias_decoding_delta function
        self.assertEqual(elias_decoding_delta(elias_delta_decode, '001010001'), 2)

class TestIndexCompression(unittest.TestCase):
    def test_index_compression(self):
        encoding_elias_gamma = {}
        # Test the overall index compression process
        total_gamma_bytes, total_inverted_bytes = encoding_elias_gamma(elias_gamma, length_gamma_id)
        total_delta_bytes = encoding_elias_delta(elias_delta, length_delta_id)
        inverted_index = decoding_elias_gamma()
        delta_index = decoding_elias_delta()

        # Test assertions for total bytes and index data correctness
        self.assertEqual(total_gamma_bytes, 10)
        self.assertEqual(total_inverted_bytes, 40)
        self.assertEqual(total_delta_bytes, 11)
        self.assertEqual(inverted_index, {'apple': [1, 3], 'banana': [2]})
        self.assertEqual(delta_index, {'apple': [1, 2, 3], 'banana': [2]})

if __name__ == '__main__':
    unittest.main()
