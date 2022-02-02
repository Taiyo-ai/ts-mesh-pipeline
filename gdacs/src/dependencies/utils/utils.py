# Python
from os import path, rename, makedirs, remove
from datetime import datetime
import shutil
import requests
import json

# own
from dependencies.utils.settings import files_root

# 3rd
import pandas as pd

base_path = files_root()


def check_file_exist(path_to_check: path):
    """
        Check if one file exists

        Parameters:
            path_to_check (path)

        Returns:
            bool
    """
    return path.exists(path_to_check)


def backup_file(path_to_backup: path, path_from_backup: path):
    """
        Backup one file

        Parameters:
            path_to_backup (path)
            path_from_backup (path)
    """
    rename(path_from_backup, path_to_backup)


def check_directories_structure():
    """
        Initial checks to create directories if missing
    """
    scraped_metadata = path.join(base_path, 'data', 'scraped_metadata')
    scraped_main_data = path.join(base_path, 'data', 'scraped_main_data')
    cleaned_main_data = path.join(base_path, 'data', 'cleaned_main_data')
    geocoded_cleaned_data = path.join(base_path, 'data', 'geocoded_cleaned_data')
    standardized_geocoded_data = path.join(base_path, 'data', 'standardized_geocoded_data')

    bk_scraped_metadata = path.join(base_path, 'backup', 'scraped_metadata')
    bk_scraped_main_data = path.join(base_path, 'backup', 'scraped_main_data')
    bk_cleaned_main_data = path.join(base_path, 'backup', 'cleaned_main_data')
    bk_geocoded_cleaned_data = path.join(base_path, 'backup', 'geocoded_cleaned_data')
    bk_standardized_geocoded_data = path.join(base_path, 'backup', 'standardized_geocoded_data')

    world_bank_data = path.join(base_path, 'world_bank')


    paths_list = [
                    scraped_metadata,
                    scraped_main_data,
                    cleaned_main_data,
                    geocoded_cleaned_data,
                    standardized_geocoded_data,
                    bk_scraped_metadata,
                    bk_scraped_main_data,
                    bk_cleaned_main_data,
                    bk_geocoded_cleaned_data,
                    bk_standardized_geocoded_data,
                    world_bank_data
                ]

    for directory in paths_list:
        if not path.exists(directory):
            makedirs(directory)


def write_json_file(file_name: str, directory_name: str, data):
    """
    Write files in json
    Backup if file exists

    Parameters:
        file_name (str): file name
        directory_name (str): directory name
        data (object): data to write
    """
    path_to_write = path.join(base_path, 'data', directory_name, file_name)
    file_exist = check_file_exist(path_to_write)

    if file_exist:

        now = datetime.now()
        now = now.strftime("%Y_%m_%d_%H_%M_%S")
        backup_name = file_name.split(".")[0] + '_' + now+'.txt'

        path_to_backup = path.join(base_path, 'backup', directory_name, backup_name)
        backup_file(path_to_backup, path_to_write)

    with open(path_to_write, 'w') as f:
        f.write(data)
        f.close()

    print('json saved on '+str(path_to_write))


def clean_directories():
    """
        Clean all files directiories to start fresh
    """
    shutil.rmtree(base_path)


def read_json_file(file_name: str, directory_name: str):
    """
    Read files and return the data in a list

    Parameters:
        file_name (str): file name
        directory_name (str): directory name

    Return:
        data (str): str with data readed
    """
    data = []
    path_to_read = path.join(base_path, 'data', directory_name, file_name)

    with open(path_to_read, 'r') as f:
        data = json.load(f)

    return data


def write_csv_file(file_name: str, directory_name: str, dataframe: pd.core.frame.DataFrame):
    """
    Write files in csv
    Backup if file exists

    Parameters:
        file_name (str): file name
        directory_name (str): directory name
        data (pandas DataFrame): data to write
    """

    path_to_write = path.join(base_path, 'data', directory_name, file_name)
    file_exist = check_file_exist(path_to_write)

    if file_exist:

        now = datetime.now()
        now = now.strftime("%Y_%m_%d_%H_%M_%S")
        backup_name = file_name.split(".")[0] + '_' + now+'.txt'

        path_to_backup = path.join(base_path, 'backup', directory_name, backup_name)
        backup_file(path_to_backup, path_to_write)

    dataframe.to_csv(path_to_write, encoding='utf-8')

    print('csv saved on '+str(path_to_write))


def read_csv_file(file_name: str, directory_name: str):
    """
    Read files and return the data in a list

    Parameters:
        file_name (str): file name
        directory_name (str): directory name

    Return:
        dataframe (padas.DataFrame): DataFrame with data
    """
    data = []
    path_to_read = path.join(base_path, 'data', directory_name, file_name)

    dataframe = pd.read_csv(path_to_read)

    return dataframe


def get_world_bank_region_data():
    """
        Query the world bank region information and download the excel file

        Returns:
            path_to_write (path): Path where the file was downloaded
    """
    filename = 'CLASS.xlsx'
    path_to_write = path.join(base_path, 'world_bank', filename)

    file_exists = check_file_exist(path_to_write)

    if file_exists:
        remove(path_to_write)

    url = 'https://databank.worldbank.org/data/download/site-content/CLASS.xlsx'
    r = requests.get(url, allow_redirects=True)
    open(path_to_write, 'wb').write(r.content)

    print('excel file saved on '+str(path_to_write))

    return path_to_write
