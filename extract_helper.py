from csv import reader, writer
from logging import getLogger

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from utils import DEBUG

"""
@BEGIN extract_text
@PARAM input_file_path
@PARAM words_output_file_path
@PARAM review_words_output_file_path
@IN wine_review_data @AS wine_review_data @URI file:{input_file_path}
@OUT words @AS words_normalized @URI file:{words_output_file_path}
@OUT review_words @AS review_words_intermediate_table @URI file:{review_words_output_file_path}
"""
def extract_text(input_file_path, words_output_file_path, review_words_output_file_path) -> None:
    """
    Extracts description from CSV
    Maps distinct word sets to row ID
    Normalizes words and assigns ID
    Passes results to be written to CSV

    Parameters
    ---
    filePath : str
        file path to data source 
    """

    """
    @BEGIN read_csv
    @DESC Read input wine review data from CSV.
    @IN input_file_path @URI file:{input_file_path}
    @OUT rows
    """
    logger = getLogger('extract_helper:extract_text')

    logger.info(f"Debug = {DEBUG}")
    logger.info("Reading CSV...")
    

    rows = read_csv(input_file_path)
    logger.info("Done.")
    """
    @END read_csv
    """

    if DEBUG:
        limit = 1000
    else:
        limit = None

    """
    @BEGIN map_description_to_freqs
    @DESC Map each review ID to the (stemmed) word count of each wine description, filtering out stopwords.
    @PARAM rows
    @OUT id_freqs @AS row_ids_mapped_to_word_frequencies
    """
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
    """
    @END map_description_to_freqs
    """

    """
    @BEGIN generate_word_ids
    @DESC Generates an ID for each distinct word that appears in a wine's description.
    @PARAM row_ids_mapped_to_word_frequencies
    @OUT word_id_map
    """
    logger.info('Generating word IDs...')
    word_id_map = generate_word_ids(id_freqs)
    logger.info('Word IDs generated.')
    """
    @END generate_word_ids
    """

    """
    @BEGIN write_word_id_rows_to_csv
    @DESC Flattens and writes word_id_map to CSV.
    @PARAM words_output_file_path
    @PARAM word_id_map
    @OUT word_id_csv @URI file:{words_output_file_path}
    """
    logger.info('Generating word ID rows...')
    words_rows = [['word_id', 'word']]
    for word, word_id in word_id_map.items():
        words_rows.append([word_id, word])
    logger.info('Word ID rows generated.')
    write_csv(words_output_file_path, words_rows)
    logger.info(f'Word ID rows written to {words_output_file_path}.')
    """
    @END write_word_id_rows_to_csv
    """

    """
    @BEGIN write_review_words_rows_to_csv
    @DESC Flattens and writes the data contained in id_freqs to CSV,
          serving as an intermediary table between the original reviews
          table and the normalized words table. 
    @PARAM row_ids_mapped_to_word_frequencies
    @PARAM review_words_output_file_path
    @PARAM review_words_rows
    @OUT review_words_csv @URI file:{review_words_output_file_path}
    """
    logger.info('Generating review_words rows...')
    review_words_rows = [['row_id', 'word_id', 'frequency']]
    for row_id, word_freq_map in id_freqs.items():
        for word, freq in word_freq_map.items():
            word_id = word_id_map[word]
            row = [row_id, word_id, freq]
            review_words_rows.append(row)
    logger.info('Generated review_words rows.')

    logger.info('Writing to CSV...')
    write_csv(review_words_output_file_path, review_words_rows)
    """
    @END write_review_words_rows_to_csv
    """

"""
@END extract_text
"""


"""
@BEGIN read_csv
@PARAM filePath
@IN csv @URI file:{filePath}
@OUT rows @AS csv_rows
"""
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
"""
@END read_csv
"""

"""
@BEGIN write_csv
@PARAM filePath
@PARAM rows
@OUT csv @AS output_csv @URI file:{filePath}
"""
def write_csv(filePath: str, rows: list) -> None:
    with open(filePath, 'w+') as f:
        w = writer(f)
        w.writerows(rows)
"""
@END write_csv
"""

"""
@BEGIN stem
@PARAM word
@OUT stemmer.stem(word) @AS stemmed_word
"""
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
"""
@END stem
"""

"""
@BEGIN is_alpha
@PARAM word
@OUT validation.issubset(allowed_chars) @AS does_word_include_only_alphabetical_characters"""
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
"""
@END is_alpha
"""

"""
@BEGIN is_stopword
@PARAM word
@OUT word in stopwords.words('english') @AS is_word_stopword
"""
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
"""
@END is_stopword
"""

"""
@BEGIN map_description_to_freqs
@PARAM description
@OUT freqs @AS word_frequency_map
"""
def map_description_to_freqs(description: str) -> dict[str: int]:
    """
    Maps words from in source descriptions to frequencies of their (stemmed) occurrence
    Discards stopwords and words with non-alphabetic characters
    """
    logger = getLogger('extract_helper:map_description_to_freqs')
    
    description = description.replace('.', '').replace('-', ' ').strip().split()
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
"""
@END map_description_to_freqs
"""

def generate_word_ids(id_freqs):
    word_id_map = {}
    word_id = 1
    for word_freq_map in id_freqs.values():
        for word in word_freq_map.keys():
            if word not in word_id_map:
                word_id_map[word] = word_id
                word_id += 1
    return word_id_map
