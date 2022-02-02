# python
from pathlib import Path
from os import path


def get_files_root() -> Path:
    """
        Gets the root files of the project
    """
    return Path(__file__).absolute().parent.parent.parent.parent.parent


def files_root():
    """
        Gets the path where all files must go
    """
    return path.join(get_files_root(), 'files')
