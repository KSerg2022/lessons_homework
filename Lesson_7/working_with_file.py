"""File functions"""

import os
import re


def get_path_to_file():
    """creates a path to the location of the file"""
    file_name = 'elements.txt'
    current_dir = os.getcwd()
    current_write_file = os.path.join(current_dir, 'examples', file_name)
    return current_write_file


def read_data_from_file(file: str) -> dict:
    """Saving information from a file into a suitable structure for further work."""
    with open(file) as f:
        read_file = []
        for line in f:
            clean_line = re.split(r',', line.rstrip(), maxsplit=1)
            read_file.append(clean_line)

        read_file_time = dict(read_file)
        values = []
        keys = []
        for key, value in read_file_time.items():
            clean_value = re.split(r',', value.rstrip())
            values.append(clean_value)
            keys.append(key)
        total_file = dict(zip(keys, values))

        return total_file


def print_info(data: str, file: dict) -> list:
    """Print result"""
    return file[data]


def read_data_from_file_to_list(file: str) -> list[list]:
    """Saving information from a file into a suitable structure for further work."""
    with open(file) as f:
        read_file = []
        for line in f:
            clean_line = re.split(r',', line.rstrip())
            line_up = [name.upper() for name in clean_line]
            read_file.append(line_up)
    return read_file
