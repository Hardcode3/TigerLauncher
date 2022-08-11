"""
This file check if the lauch of TIGER works.
It may not wor under certain IDEs like Pycharm.
Run it from bash.
"""
import subprocess


def test(sample_file: str) -> bool:
    process = subprocess.run(['mpirun', '-n', '2', 'tiger-opt', '-i', sample_file], capture_output=True, text=True)
    if process.returncode == 0:
        return True
    return False


if __name__ == '__main__':
    test()
