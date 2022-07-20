# Winery Dataset Description Text Extraction
This script was developed by Tyler Davis as part of the CS 513 group project on the Kaggle wine review dataset.

This script was developed for Python 3.9.2.

## Usage
0. Optional: Start up a virtual environment to contain this project. This project will download additional corpora files from the Natural Language Toolkit and a virtual environment will keep them (and other Python packages) isolated from the rest of your platform.

1. Install the script's dependencies:

```sh
pip install -r requirements.txt
```

2. Run the script:
```sh
python extract.py
```
Source data files are stored in the `data` directory. Output data files are written to the same directory. Text extraction may take a long time due to the size of the source dataset.

3. For project submission: Extract relevant files for submission by running
`python package.py`. 


## Data
Within the `./data` directory there will be at most three files. If the script has not ran to completion, only the raw source data `winemag-data-130k-v2.csv` will be in the directory. 

After the script has ran to completion, two other CSV files will have been saved alongside the source data:
* `words.csv`
    * This is the normalized table for words extracted from wine reviews. Each unique word appearing in the source data appears in this table exactly once.
* `review_words.csv`
    * This is the intermediary table linking the normalized words table with the source data. Each row consists of three values: a row ID from the source data, a word ID from the normalized words table, and a frequency indicating how many times a word was used within a given review.

The benefit of this data structure is its flexibility. For example, we can now either use the intermediary table to analyze the frequencies of words appearing within a single review or we can aggregate the words in the normalized `words` table to find which words are most common across the entire dataset.
