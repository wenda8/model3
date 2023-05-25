import unittest
import pymorphy2
import nltk
import re
from new_clean import clean_word

class TestCleanWord(unittest.TestCase):
    def setUp(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.only_alpha = nltk.tokenize.RegexpTokenizer('[а-яА-ЯЁё]+')

    def test_cyrillic(self):
        text = 'проверка'
        result = clean_word(text)
        self.assertEqual(result, ['проверка'])
        text = 'ректор'
        result = clean_word(text)
        self.assertEqual(result, ['ректор'])
        text = 'спбгу'
        result = clean_word(text)
        self.assertEqual(result, ['спбгу'])
        text = 'мгу'
        result = clean_word(text)
        self.assertEqual(result, ['мгу'])
        text = 'текст'
        result = clean_word(text)
        self.assertEqual(result, ['текст'])

    def test_latin(self):
        text = 'test'
        result = clean_word(text)
        self.assertEqual(result, [])
        text = 'spbu'
        result = clean_word(text)
        self.assertEqual(result, [])
        text = 'msu'
        result = clean_word(text)
        self.assertEqual(result, [])
        text = 'clean'
        result = clean_word(text)
        self.assertEqual(result, [])
        text = 'word'
        result = clean_word(text)
        self.assertEqual(result, [])

    def test_punctuation(self):
        text = 'проверка, проверка!'
        result = clean_word(text)
        self.assertEqual(result, ['проверка', 'проверка'])
        text = '!!//??..""";;;'
        result = clean_word(text)
        self.assertEqual(result, [])
        text = '//ректор спбгу!//'
        result = clean_word(text)
        self.assertEqual(result, ['ректор', 'спбгу'])
        text = 'проверка выполнена!'
        result = clean_word(text)
        self.assertEqual(result, ['проверка', 'выполнить'])
        text = 'высокого;.'';,.*/-+'
        result = clean_word(text)
        self.assertEqual(result, ['высокий'])

    def test_whitespace(self):
        text = 'проверка  проверка'
        result = clean_word(text)
        self.assertEqual(result, ['проверка', 'проверка'])
        text = '       '
        result = clean_word(text)
        self.assertEqual(result, [])
        text = 's a d j v p a s'
        result = clean_word(text)
        self.assertEqual(result, [])
        text = 'проверка  test  测试'
        result = clean_word(text)
        self.assertEqual(result, ['проверка'])
        text = 'проверка * проверка'
        result = clean_word(text)
        self.assertEqual(result, ['проверка', 'проверка'])

    def test_lowercase(self):
        text = 'ПРОВЕРКА'
        result = clean_word(text)
        self.assertEqual(result, ['проверка'])
        text = 'Ректор'
        result = clean_word(text)
        self.assertEqual(result, ['ректор'])
        text = 'СПБГУ'
        result = clean_word(text)
        self.assertEqual(result, ['спбгу'])
        text = 'МГУ'
        result = clean_word(text)
        self.assertEqual(result, ['мгу'])
        text = 'SPBU'
        result = clean_word(text)
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
