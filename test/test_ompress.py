import unittest
from new_compress import elias_coding_gamma, elias_decoding_gamma, elias_coding_delta, elias_delta_decode, elias_decoding_delta

class TestEliasCoding(unittest.TestCase):
    def test_elias_coding_gamma(self):
        self.assertEqual(elias_coding_gamma(1), '1')
        self.assertEqual(elias_coding_gamma(2), '010')
        self.assertEqual(elias_coding_gamma(5), '00101')
        self.assertEqual(elias_coding_gamma(10), '0001010')
        self.assertEqual(elias_coding_gamma(10000), '000000000000010011100010000')

    def test_elias_decoding_gamma(self):
        self.assertEqual(elias_decoding_gamma('1'), 1)
        self.assertEqual(elias_decoding_gamma('010'), 2)
        self.assertEqual(elias_decoding_gamma('00101'), 5)
        self.assertEqual(elias_decoding_gamma('0001010'), 10)
        self.assertEqual(elias_coding_gamma(10000), '000000000000010011100010000')

    def test_elias_coding_delta(self):
        self.assertEqual(elias_coding_delta(1), '1')
        self.assertEqual(elias_coding_delta(2), '0100')
        self.assertEqual(elias_coding_delta(5), '01101')
        self.assertEqual(elias_coding_delta(10), '00100010')
        self.assertEqual(elias_coding_delta(10000), '00011100011100010000')

    def test_elias_delta_decode(self):
        self.assertEqual(elias_delta_decode([1]), 1)
        self.assertEqual(elias_delta_decode([0, 1, 0, 0]), 2)
        self.assertEqual(elias_delta_decode([0, 1, 1, 0, 1]), 5)
        self.assertEqual(elias_delta_decode([0, 0, 1, 0, 0, 0, 1, 0]), 10)
        self.assertEqual(elias_delta_decode([0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,1,0,0,0,0]), 10000)

    def test_elias_decoding_delta(self):
        self.assertEqual(elias_decoding_delta(elias_delta_decode, '1'), 1)
        self.assertEqual(elias_decoding_delta(elias_delta_decode, '0100'), 2)
        self.assertEqual(elias_decoding_delta(elias_delta_decode, '01101'), 5)
        self.assertEqual(elias_decoding_delta(elias_delta_decode, '00100010'), 10)
        self.assertEqual(elias_decoding_delta(elias_delta_decode, '00011100011100010000'), 10000)

if __name__ == '__main__':
    unittest.main()
