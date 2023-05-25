import unittest
import os
import json
import pickle
from new_bulid_index import divide_to_txt, build_inverted_index, save_index

class TestIndexBuilder(unittest.TestCase):

    def setUp(self):
        self.csv_file_name = 'test_data.csv'
        self.csv_file_name_single = 'test_data_1.csv'
        self.folder_path = 'test_folder'
        self.file_index = {}
        self.inverted_index = {}
        os.makedirs(self.folder_path, exist_ok=True)


    def test_divide_to_txt_single_document(self):
        # Prepare
        expected_filename = '92_2023-02-14.txt'
        expected_file_path = os.path.join(self.folder_path, expected_filename)

        # Execute
        file_index, index = divide_to_txt(self.csv_file_name, self.file_index, 1, self.folder_path)

        # Assert
        self.assertIn(1, file_index)
        self.assertEqual(file_index[1], expected_filename)
        self.assertEqual(index, 4)
        self.assertTrue(os.path.exists("test_folder/92_2023-02-14.txt"))
        with open(expected_file_path, 'r', encoding='utf-8') as txt_file:
            content = txt_file.read()
            for row in content:
                self.assertIn(','.join(row), content)


   
    def test_build_inverted_index_single_document(self):
        # Prepare
        self.file_index = {}
        expected_inverted_index = {'весна': [1], 'ещё': [1], 'с': [1], 'из': [1], 'макролинза': [1], 'садмгу': [1], 'фотография': [1], 'снятой': [1], 'мгу': [1], 'часть': [1], 'сад': [1], 'ботаническийсад': [1], 'ботанический': [1], 'ранняявесный': [1], 'ранний': [1], 'несколько': [1]}

        self.file_index, self.index = divide_to_txt(self.csv_file_name_single, self.file_index, 1, self.folder_path)

        # Execute
        self.inverted_index = build_inverted_index(self.file_index, self.inverted_index, self.folder_path)

        # Assert
        self.assertTrue(self.inverted_index == expected_inverted_index)

    def test_divide_to_txt_multiple_documents(self):
        # Prepare
        rows = [['92', '2023-02-14'], ['593', '2023-03-04'], ['5283', '2023-01-17']]
        expected_filenames = ['92_2023-02-14.txt', '593_2023-03-04.txt', '5283_2023-01-17.txt']

        # Execute
        file_index, index = divide_to_txt(self.csv_file_name, self.file_index, 1, self.folder_path)

        # Assert
        self.assertEqual(len(file_index), 3)
        for i, filename in file_index.items():
            self.assertIn(filename, expected_filenames)
        self.assertEqual(index, 4)
        for filename in expected_filenames:
            file_path = os.path.join(self.folder_path, filename)
            self.assertTrue(os.path.exists(file_path))
            with open(file_path, 'r', encoding='utf-8') as txt_file:
                content = txt_file.read()
                for row in content:
                    self.assertIn(','.join(row), content)

    def test_build_inverted_index_multiple_documents(self):
        # Prepare
        self.file_index[1] = '92_2023-02-14.txt'
        self.file_index[2] = '593_2023-03-04.txt'
        self.file_index[3] = '5283_2023-01-17.txt'
        expected_inverted_index = {'снятой': [1], 'ещё': [1], 'с': [1], 'из': [1, 3], 'макролинза': [1], 'садмгу': [1], 'мгу': [1, 2], 'часть': [1], 'несколько': [1], 'ботанический': [1], 'ботаническийсад': [1], 'ранний': [1], 'фотография': [1], 'весна': [1, 2], 'сад': [1], 'ранняявесный': [1], 'на': [2], 'выступить': [2], 'студенческий': [2], 'в': [2, 3], 'силуэтмга': [2], 'конкурс': [2], 'они': [3], 'о': [3], 'конец': [3], 'пора': [3], 'память': [3], 'библиотекавыкса': [3], 'всё': [3], 'так': [3], 'современный': [3], 'неугодный': [3], 'писатель': [3], 'справедливость': [3], 'х': [3], 'литературовед': [3], 'многочисленный': [3], 'белые': [3], 'и': [3], 'сложный': [3], 'автор': [3], 'персона': [3], 'календарь': [3], 'забыть': [3], 'литературный': [3], 'историк': [3], 'варлам': [3], 'сей': [3], 'пятно': [3], 'который': [3], 'жертва': [3], 'поговорить': [3], 'эпизод': [3], 'хотеть': [3], 'бороться': [3], 'центральный': [3], 'немой': [3], 'прожить': [3], 'неизвестный': [3], 'любопытный': [3], 'факт': [3], 'год': [3], 'поэтому': [3], 'чтобы': [3], 'слишком': [3], 'жизнь': [3], 'многий': [3], 'оставаться': [3], 'особенно': [3], 'вообще': [3], 'сегодня': [3], 'быть': [3], 'многие': [3], 'шаламов': [3], 'до': [3], 'за': [3], 'биография': [3]}
        # Execute
        self.file_index, self.index = divide_to_txt(self.csv_file_name, self.file_index, 1, self.folder_path)
        self.inverted_index = build_inverted_index(self.file_index, self.inverted_index, "test_folder")
        #assert
        self.assertTrue(self.inverted_index == expected_inverted_index)
    def test_save_index(self):
        # Prepare
        expected_file_index = {'1': '92_2023-02-14.txt', '2': '593_2023-03-04.txt','3': '5283_2023-01-17.txt'}
        expected_inverted_index = {'снятой': [1], 'ещё': [1], 'с': [1], 'из': [1, 3], 'макролинза': [1], 'садмгу': [1], 'мгу': [1, 2], 'часть': [1], 'несколько': [1], 'ботанический': [1], 'ботаническийсад': [1], 'ранний': [1], 'фотография': [1], 'весна': [1, 2], 'сад': [1], 'ранняявесный': [1], 'на': [2], 'выступить': [2], 'студенческий': [2], 'в': [2, 3], 'силуэтмга': [2], 'конкурс': [2], 'они': [3], 'о': [3], 'конец': [3], 'пора': [3], 'память': [3], 'библиотекавыкса': [3], 'всё': [3], 'так': [3], 'современный': [3], 'неугодный': [3], 'писатель': [3], 'справедливость': [3], 'х': [3], 'литературовед': [3], 'многочисленный': [3], 'белые': [3], 'и': [3], 'сложный': [3], 'автор': [3], 'персона': [3], 'календарь': [3], 'забыть': [3], 'литературный': [3], 'историк': [3], 'варлам': [3], 'сей': [3], 'пятно': [3], 'который': [3], 'жертва': [3], 'поговорить': [3], 'эпизод': [3], 'хотеть': [3], 'бороться': [3], 'центральный': [3], 'немой': [3], 'прожить': [3], 'неизвестный': [3], 'любопытный': [3], 'факт': [3], 'год': [3], 'поэтому': [3], 'чтобы': [3], 'слишком': [3], 'жизнь': [3], 'многий': [3], 'оставаться': [3], 'особенно': [3], 'вообще': [3], 'сегодня': [3], 'быть': [3], 'многие': [3], 'шаламов': [3], 'до': [3], 'за': [3], 'биография': [3]}
        expected_file_index_json = 'file_index.json'
        expected_inverted_index_json = 'inverted_index.json'
        expected_file_index_pkl = 'file_index.pkl'
        expected_inverted_index_pkl = 'inverted_index.pkl'

        # Execute
        save_index(expected_file_index, expected_inverted_index)

        # Assert
        self.assertTrue(os.path.exists(expected_file_index_json))
        self.assertTrue(os.path.exists(expected_inverted_index_json))
        self.assertTrue(os.path.exists(expected_file_index_pkl))
        self.assertTrue(os.path.exists(expected_inverted_index_pkl))
        with open(expected_file_index_json, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            self.assertEqual(json_data, expected_file_index)
        with open(expected_inverted_index_json, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            self.assertEqual(json_data, expected_inverted_index)
        with open(expected_file_index_pkl, 'rb') as file:
            pickle_data = pickle.load(file)
            self.assertEqual(pickle_data, expected_file_index)
        with open(expected_inverted_index_pkl, 'rb') as file:
            pickle_data = pickle.load(file)
            self.assertEqual(pickle_data, expected_inverted_index)
        

    def tearDown(self):
        if os.path.exists(self.folder_path):
            for filename in os.listdir(self.folder_path):
                file_path = os.path.join(self.folder_path, filename)
                os.remove(file_path)
            os.rmdir(self.folder_path)
        if os.path.exists('file_index.json'):
            os.remove('file_index.json')
        if os.path.exists('inverted_index.json'):
            os.remove('inverted_index.json')
        if os.path.exists('file_index.pkl'):
            os.remove('file_index.pkl')
        if os.path.exists('inverted_index.pkl'):
            os.remove('inverted_index.pkl')

def run_tests():
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIndexBuilder)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == '__main__':
    run_tests()