# Copyright 2019 George Le
from pathlib import Path

def write_to_file(filename = str(), output = str(), directory = str()):
    if len(directory) == 0 and len(filename) > 0:
       with open(filename, 'w', encoding='utf-8') as f:
            f.write(output)
    elif len(directory) > 0 and len(filename) > 0:
        pass

def check_directory(directory_path, filename):
    config = Path(directory_path + filename)
    if config.is_file():
        return True
    else:
        return False