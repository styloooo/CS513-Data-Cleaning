import unittest
from extract_helper import read_csv
from utils import DATA_FILE_PATH

class ExtractTests(unittest.TestCase):
    
    def test_read_csv(self):
        rows = read_csv(DATA_FILE_PATH)
        self.assertEquals(len(rows), 129972 - 1)  # excludes header

if __name__ == '__main__':
    unittest.main()
