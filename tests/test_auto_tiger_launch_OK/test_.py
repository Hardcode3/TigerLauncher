"""
This file checks if the class AutoTigerLaunch is working with the actual configuration.
It may not wor under certain IDEs like Pycharm.
Run it from bash.
"""
from pathlib import Path
import _io
import sys

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from typing import Callable
from tiger_launcher.auto_tiger_launch import AutoTigerLaunch
from tiger_launcher.misc_functions import get_time


def log(func: Callable) -> Callable:
    def wrapper():
        # open a log file for the python console: this file will help if there are issues related to the python code
        # a python log is created everytime this main file is launched
        # (date and hour is inscribed in its name under the logs' folder)
        pylog = open(f"test_auto_tiger_launch_pylog.txt", "w")
        success = func(pylog)
        pylog.close()
        return success

    return wrapper


@log
def test(pylog: _io.TextIOWrapper) -> bool:
    return AutoTigerLaunch(pylog, 2).success
   

if __name__ == '__main__':
    # put input files into the input directory for the test to work
    test()
    
