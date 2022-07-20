import os
import shutil

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

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    else:
        shutil.rmtree(OUTPUT_DIR)
        os.mkdir(OUTPUT_DIR)

    for path, fileName in FILE_PATHS.items():
        output_path = os.path.join(OUTPUT_DIR, fileName)
        shutil.copy(path, output_path)

if __name__ == '__main__':
    main()
