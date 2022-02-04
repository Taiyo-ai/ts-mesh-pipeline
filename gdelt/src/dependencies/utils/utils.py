# Python packages
from pathlib import Path
from os import path, makedirs
import shutil
import json

data_root = Path(__file__).absolute().parent.parent.parent.parent
base_path = path.join(data_root, 'data')


def initialize_directories():
    scraped_main_data = path.join(base_path, 'scraped_main_data')
    cleaned_main_data = path.join(base_path, 'cleaned_main_data')
    geocoded_main_data = path.join(base_path, 'geocoded_main_data')
    standardized_main_data = path.join(
        base_path, 'standardized_main_data'
    )

    directories_list = [
        scraped_main_data,
        cleaned_main_data,
        geocoded_main_data,
        standardized_main_data,
    ]

    for directory in directories_list:
        if not path.exists(directory):
            makedirs(directory)

    return None


def save_json_file(json_file: json, directory_name: str, file_name: str):
    absolute_path = path.join(base_path, directory_name, file_name)

    with open(absolute_path, 'w') as f:
        f.write(json_file)
        f.close()

    return None


def read_json_file(directory_name: str, file_name: str):
    json_path = path.join(base_path, directory_name, file_name)
    json_file = []

    with open(json_path, 'r') as f:
        json_file = json.load(f)

    return json_file


def empty_directories():
    shutil.rmtree(base_path)

    return None
