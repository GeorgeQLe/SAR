# Copyright 2019 George Le
import os
from pathlib import Path

def add_endslash(directory_path = str()):
    if len(directory_path) == 0:
        return directory_path
    elif len(directory_path) > 0:
        if directory_path[len(directory_path) - 1] == '/':
            return directory_path
    return directory_path + "/"

def write_to_file(filename = str(), output = str(), directory = str()):
    if len(directory) == 0 and len(filename) > 0:
       with open(filename, 'a', encoding='utf-8') as f:
            f.write(output)
    elif len(directory) > 0 and len(filename) > 0:
        if valid_path(file_path = directory+filename):
            with open(directory+filename, 'a', encoding='utf-8') as f:
                f.write(output)

def valid_directory(directory_path = str(), filename = str()):
    if len(directory_path) == 0:
        print("ERROR: DIRECTORY_PATH EMPTY")
        return False

    if len(filename) > 0:
        config = Path(directory_path + filename)
        if config.is_file():
            return True
        else:
            return False
    else:
        return os.path.isdir(directory_path)

def valid_path(file_path = str()):
    if len(file_path) == 0:
        return False

    config = Path(file_path)
    return config.is_file()