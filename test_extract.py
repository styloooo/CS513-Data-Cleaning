import unittest

from os import path, remove

from extract_helper import read_csv, write_csv
from utils import DATA_FILE_PATH, TEST_DATA_DIR

class CsvTests(unittest.TestCase):

    write_path = path.join(TEST_DATA_DIR, 'test_write_csv.csv')

    @classmethod
    def tearDownClass(cls):
        remove(cls.write_path)

    def test_read_csv(self):
        rows = read_csv(DATA_FILE_PATH)
        self.assertEquals(len(rows), 129972 - 1)  # excludes header

    def test_write_csv(self):
        rows = [
            [1, 2, 3, 4],
            ['A', 'B', 'C', 'D'],
            ['foo', 'bar', 'spam', 'eggs']
        ]

        write_csv(type(self).write_path, rows)
        # self.assert

class TextProcessingTests(unittest.TestCase):
    
    def test_stemmer(self):
        pass

    def test_stopword_detection(self):
        pass

class WordIdTests(unittest.TestCase):

    # Testing generated Word ID functional dependency (PKs)
    def test_word_id_fd(self):
        pass

if __name__ == '__main__':
    unittest.main()
