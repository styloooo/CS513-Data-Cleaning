import os
import shutil
import logging
from utils import (DATA_FILE_PATH, DATA_FILE_NAME,
                   WORDS_FILE_NAME, WORDS_FILE_PATH,
                   REVIEW_WORDS_FILE_NAME, REVIEW_WORDS_FILE_PATH)

BASE_DIR = os.getcwd()
FILE_NAMES = (
    'extract_helper.py',
    'extract.py',
    'README.md',
    'requirements.txt',
    'utils.py',
    'Workflow.gv',
    'Workflow.pdf',
    'Workflow.yw',
    'yw-graph.sh',
    'package.py'
    )

FILE_PATHS = {os.path.join(BASE_DIR, fName): fName for fName in FILE_NAMES}
OUTPUT_DIR = os.path.join(BASE_DIR, 'text-extract-packaged')
OUTPUT_DATA_DIR = os.path.join(OUTPUT_DIR, 'data')
INPUT_DATA_FILE_PATH = os.path.join(OUTPUT_DATA_DIR, DATA_FILE_NAME)

DATA_FILE_PATHS = {
    DATA_FILE_PATH: DATA_FILE_NAME,
    WORDS_FILE_PATH: WORDS_FILE_NAME,
    REVIEW_WORDS_FILE_PATH: REVIEW_WORDS_FILE_NAME
}

def main():
    logger = logging.getLogger('package')
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    if not os.path.exists(OUTPUT_DATA_DIR):
        os.makedirs(OUTPUT_DATA_DIR)
    else:
        shutil.rmtree(OUTPUT_DATA_DIR)
        os.makedirs(OUTPUT_DATA_DIR)

    for path, fileName in FILE_PATHS.items():
        output_path = os.path.join(OUTPUT_DIR, fileName)
        shutil.copy(path, output_path)

    for path, fileName in DATA_FILE_PATHS.items():
        if not os.path.exists(path):
            logger.warning(f"Source file {path} not found.")
            continue
        output_path = os.path.join(OUTPUT_DATA_DIR, fileName)
        shutil.copy(path, output_path)

if __name__ == '__main__':
    main()
