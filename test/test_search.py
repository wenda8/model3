import unittest
import json
from new_search import search_data

class TestSearchData(unittest.TestCase):

    def setUp(self):
        with open('inverted_index.json', 'r') as jsonfile:
            self.inverted_index_search = json.load(jsonfile)
        self.func = search_data

    def test_single_match(self):
        # проверка единственного вхождения
        for i in range(5):
            # 使用已知的关键字进行测试，这个关键字只在json文件中出现一次
            self.assertEqual(self.func('word1'), self.inverted_index_search['word1'])
    
    def test_multiple_match(self):
        # проверка множественного вхождения
        for i in range(5):
            # 使用已知的关键字进行测试，这个关键字在json文件中出现多次
            self.assertEqual(self.func('word3'), self.inverted_index_search['word3'])
    
    def test_empty_string(self):
        # проверка пустой строки
        for i in range(5):
            # 使用空字符串进行测试，期望返回None
            self.assertIsNone(self.func(''))

if __name__ == '__main__':
    unittest.main()
