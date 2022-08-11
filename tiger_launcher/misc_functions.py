"""
File containing miscellaneous functions for the project.
"""

import datetime


def pythonLog(file, arg: str, v: bool = True) -> None:
    """
    Creates a python log file under the log folder and also prints in the python console.
    """
    if isinstance(arg, str):
        if v:
            print(arg)
        file.write(arg)


def get_time() -> str:
    """
    Format and returns the time to add it into log file's names
    """
    return datetime.datetime.now().strftime("%Y-%m-%d_@_%H:%M:%S")
