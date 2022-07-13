import logging

from os import environ, path
from platform import system
from nltk import download
from nltk.data import find

from extract_helper import extract_text
from utils import (
    DATA_FILE_PATH,
    REQUIRED_NLTK_PACKAGES,
    REVIEW_WORDS_FILE_PATH,
    WORDS_FILE_PATH
)

def main():
    """
    Installs platform-specific NLTK dependencies before starting text extraction
    """
    logger = logging.getLogger('extract')

    if 'VIRTUAL_ENV' in environ.keys():
        download_dir = path.join(environ['VIRTUAL_ENV'], 'nltk_data')
    elif system() == 'Darwin':
        download_dir = '/usr/share/nltk_data'
    elif system() == 'Windows':
        download_dir = 'C:/nltk_data'
    elif system() == 'Linux':
        download_dir = '/usr/share/nltk_data'
    else:
        raise RuntimeError("Unrecognized system architecture: can't install nltk_data")

    for full_pkg_name, short_pkg_name in REQUIRED_NLTK_PACKAGES.items():
        try:
            find(full_pkg_name)
        except LookupError:
            logger.info(f"Downloading NLTK package {full_pkg_name}...")
            download(short_pkg_name,  download_dir=download_dir)

    FORMAT = '[%(levelname)s] %(asctime)s %(lineno)d: %(message)s'
    logging.basicConfig(format=FORMAT, level='DEBUG')

    extract_text(DATA_FILE_PATH, WORDS_FILE_PATH, REVIEW_WORDS_FILE_PATH)

if __name__ == '__main__':
    main()
