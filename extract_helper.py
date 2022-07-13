from csv import reader, writer
from logging import getLogger

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from utils import DEBUG

def read_csv(filePath: str) -> list[list[str, str]]:
    """
    Read CSV on disk

    Parameters
    ----
    filePath : str
        path to data source on disk

    Returns
    ----
    list[list[str, str]]
        A list of lists each containing a row ID and
        corresponding description text
    """
    rows = []
    with open(filePath, 'r') as f:
        r = reader(f)
        for idx, row in enumerate(r):
            if idx == 0:
                continue  # skip header
            outRow = [row[0], row[2]]
            rows.append(outRow)
    return rows

def write_csv(filePath: str, rows: list) -> None:
    with open(filePath, 'w+') as f:
        w = writer(f)
        w.writerows(rows)

def stem(word) -> str:
    """
    Stems a single word using the NLTK's Snowball Stemmer

    Parameters
    ---
    word : str
        text to stem

    Returns
    ---
    str
        Stemmed text
    """
    stemmer = SnowballStemmer('english')
    return stemmer.stem(word)

def is_alpha(word):
    """
    Determines whether a word contains non-alphabetic characters
    Parameters
    ---
    word : str
        String of word to check for non-alphabetic characters

    Returns
    ---
    bool
        True if word only consists of alphabetic characters
    """
    # return word.isalpha()
    allowed_chars = set(("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'"))
    validation = set((word))
    return validation.issubset(allowed_chars)

def is_stopword(word):
    """
    Determines whether a word is a stopword based on NLTK's stopword corpus
    
    Parameters
    ---
    word : str
        String of word to check whether it is a stopword

    Returns
    ---
    bool
        True if word is stopword
    """
    return word in stopwords.words('english')

def map_description_to_freqs(description: str) -> dict[str: int]:
    """
    Maps words from in source descriptions to frequencies of their (stemmed) occurrence
    Discards stopwords and words with non-alphabetic characters
    """
    logger = getLogger('extract_helper:map_description_to_freqs')
    
    description = description.replace('.', '').strip().split()
    freqs = {}

    for word in description:
        word = word.lower()
        if is_stopword(word) or not is_alpha(word):
            continue  # this string contains non-alphabetic characters or is a stopword so we discard
        stemmedWord = stem(word)
        if stemmedWord in freqs.keys():
            freqs[stemmedWord] += 1
        else:
            freqs[stemmedWord] = 1

    return freqs

def extract_text(input_file_path, words_output_file_path, review_words_output_file_path) -> None:
    """
    Extracts description from CSV
    Maps distinct word sets to row ID
    Passes results to be written to CSV

    Parameters
    ---
    filePath : str
        file path to data source 
    """
    logger = getLogger('extract_helper:extract_text')

    logger.info("Reading CSV...")
    rows = read_csv(input_file_path)
    logger.info("Done.")
    
    if DEBUG:
        limit = 1000
    else:
        limit = None
    logger.info(f"Debug = {DEBUG}")
    logger.info("Mapping word frequencies...")
    id_freqs = {}
    for row in rows[:limit]:
        row_id = int(row[0])
        logger.info(f"processing row_id {row_id}...")
        description = row[1]
        if row_id not in id_freqs:
            id_freqs[row_id] = map_description_to_freqs(description)
        else:
            logger.warn(f"Duplicate ID {row_id} found while mapping freqs - additional row skipped")
    logger.info("Done.")

    logger.info('Generating word IDs...')
    word_id_map = {}
    word_id = 1
    for word_freq_map in id_freqs.values():
        for word in word_freq_map.keys():
            if word not in word_id_map:
                word_id_map[word] = word_id
                word_id += 1
    logger.info('Word IDs generated.')

    logger.info('Generating word ID rows...')
    words_rows = [['word_id', 'word']]
    for word, word_id in word_id_map.items():
        words_rows.append([word_id, word])
    logger.info('Word ID rows generated.')

    logger.info('Generating review_words rows...')
    review_words_rows = [['row_id', 'word_id', 'frequency']]
    for row_id, word_freq_map in id_freqs.items():
        for word, freq in word_freq_map.items():
            word_id = word_id_map[word]
            row = [row_id, word_id, freq]
            review_words_rows.append(row)
    logger.info('Generated review_words rows.')

    logger.info('Writing to CSV...')
    write_csv(words_output_file_path, words_rows)
    write_csv(review_words_output_file_path, review_words_rows)
