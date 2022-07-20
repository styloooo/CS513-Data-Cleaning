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

Source data files are stored in the `data` directory. Output data files are written to the same directory.

Note: Extraction may take a long time due to the size of the source dataset.
