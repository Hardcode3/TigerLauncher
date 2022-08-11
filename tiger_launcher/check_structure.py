"""
This file is responsible for verification of the project's structure.
"""
import os

WORKING_DIRECTORY = os.path.abspath("")


def check_structure() -> None:
    """
    Checks the structure of the project and correct it if necessary.
    Avoids FileNotExists and other errors.
    """
    if not os.path.exists(os.path.join(WORKING_DIRECTORY, 'output')):
        os.mkdir(os.path.join(WORKING_DIRECTORY, 'output'))
    if not os.path.exists(os.path.join(WORKING_DIRECTORY, 'input')):
        os.mkdir(os.path.join(WORKING_DIRECTORY, 'input'))
    if not os.path.exists(os.path.join(WORKING_DIRECTORY, 'logs')):
        os.mkdir(os.path.join(WORKING_DIRECTORY, 'logs'))


if __name__ == '__main__':
    check_structure()
