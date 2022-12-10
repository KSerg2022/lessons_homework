"""Modul to read data from file."""
import json
import os


def read_data_from_file():
    """Read data from file."""
    current_dir = os.getcwd()
    path_to_file = current_dir + '/static/data.json'
    with open(path_to_file, encoding='UTF-8') as f:
        data = json.load(f)
    return data


ALL_DATA = read_data_from_file()
CITIES_NAME = ALL_DATA.keys()

