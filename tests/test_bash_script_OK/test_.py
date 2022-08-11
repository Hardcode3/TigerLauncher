"""
This file check if the lauch of TIGER works.
It may not wor under certain IDEs like Pycharm.
Run it from bash.
"""
from pathlib import Path
import sys
path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))
import subprocess
from settings import TIGER_PATH


def test(sample_file: str) -> bool:
    process = subprocess.run(['mpirun', '-n', '2', TIGER_PATH, '-i', sample_file], capture_output=True, text=True)
    if process.returncode == 0:
        return True
    return False


if __name__ == '__main__':
    test()
