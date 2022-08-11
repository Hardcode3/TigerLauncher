"""
This main script is the entry point to launch TIGER simulations under the MOOSE framework.
Python version should be 3.10 or newer.
TIGER should already work and be tested and can be added to path to facilitate the use of the code.
"""
import _io
import sys
from typing import Callable

from tiger_launcher.auto_tiger_launch import AutoTigerLaunch
from tiger_launcher.auto_duplicate_tiger_input_file import AutoDuplicateTigerInputFile
from tiger_launcher.misc_functions import get_time
from tiger_launcher.check_structure import check_structure
from settings import TIGER_PATH

sys.path.append('tiger_launcher')
sys.path.append('tiger_launcher/command')
sys.path.append('tiger_launcher/get_project_root')

def log(launch: Callable) -> Callable:
    def wrapper():
        # open a log file for the python console: this file will help if there are issues related to the python code
        # a python log is created everytime this main file is launched
        # (date and hour is inscribed in its name under the logs' folder)
        check_structure()
        pylog = open(f'logs/pylog_{get_time()}.txt', 'w')
        launch(pylog)
        pylog.close()

    return wrapper


@log
def run(pylog: _io.TextIOWrapper) -> None:
    # FIRST CHOOSE THE RANGE OF VALUES YOU WANT TO PLAY WITH IN THE SETTINGS PYTHON FILE
    #   -> file to modify : settings.py
    # THEN, ALWAYS IN THE SAME FILE, ENTER THE FILES YOU DO NOT WANT TO ANALYZE

    # PREPARE THE SINGLE INPUT FILE THAT WILL BE DUPLICATED WITH THE SPECIFIED PARAMETERS BY :
    # 1- WRITING '#FAULTPERMEA' IN COMMENT AT THE LINE CORRESPONDING TO THE FAULT PERMEABILITY
    # 2- WRITING '#FAULTTHICKNESS' IN COMMENT AT THE LINE CORRESPONDING TO THE FAULT THICKNESS
    # 3- WRITING '#FAULTCOMPRESSIBILITY' IN COMMENT AT THE LINE CORRESPONDING TO THE FAULT COMPRESSIBILITY
    # 4- WRITING '#FAULTPORO' IN COMMENT AT THE LINE CORRESPONDING TO THE FAULT POROSITY
    # 5- WRITING '#OUTPUTNAME' IN COMMENT AT THE LINE CORRESPONDING TO THE OUTPUT NAME IN ORDER FOR THE CODE
    #       TO CREATE DIFFERENT NAMES FOR THE OUTPUT FILES
    # !!! IF #OUTPUTNAME IS NOT SPECIFIED, THEN A SINGLE FILE WIL BE CREATED AND REPLACED EVERY TIME A NEW
    #       SIMULATION BEGIN

    # for comparison purposes, put the experimental data into the folder well data (optional)

    # CHOOSE THE INPUT FILE YOU WANT TO WORK ON (only if you need to duplicate an input file)

    inputFile = ''

    # THE INPUT FILE WILL BE DUPLICATED AND THE VALUES REPLACED FOR EVERY PARAMETER'S COMBINATION

    # AutoDuplicateTigerInputFile(inputFile, pylog, verbose=True)
    
    # SOME .i FILES SHOULD HAVE APPEARED IN THE input
    # information about the specified parameters should appear in their name, such as:
    #       blablablaTH3cal@permea@thickness@compressibility@poro.i
    # every output file will be saved under the output folder with the same name
    # IF THE FILES WERE MANUALLY MODIFIED, JUST COMMENT THE TWO LAST COMMANDS

    # specify the directory of the TIGER executable (tiger-opt) to run th simulations (in settings.py)

    # the following command will run every files under the input directory in an automatic way
    # the files will be listed and their number will be displayed
    # select verbose to see details about the current state of the simulation
    # select runSimu to run the TIGER simulations through terminal, otherwise the files will only be duplicated
    #   based on the file settings.py
    AutoTigerLaunch(pylog, verbose=True)


if __name__ == '__main__':
    run()
