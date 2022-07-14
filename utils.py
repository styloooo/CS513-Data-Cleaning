from os import path, getcwd

# Data File Paths (In/Output)
DATA_DIR = path.join(getcwd(), 'data')
DATA_FILE_NAME = 'winemag-data-130k-v2.csv'
DATA_FILE_PATH = path.join(DATA_DIR, DATA_FILE_NAME)
WORDS_FILE_NAME = 'words.csv'
WORDS_FILE_PATH = path.join(DATA_DIR, WORDS_FILE_NAME)
REVIEW_WORDS_FILE_NAME = 'review_words.csv'
REVIEW_WORDS_FILE_PATH = path.join(DATA_DIR, REVIEW_WORDS_FILE_NAME)

# NLTK Config
REQUIRED_NLTK_PACKAGES = {
    'corpora/stopwords': 'stopwords'
}

# Debug
DEBUG = True

# Test configs
TEST_DATA_DIR = path.join(getcwd(), 'test_data')
