import sys
from pathlib import Path

path_root = Path(__file__).parents[2]
sys.path.append(str(path_root))

from tiger_launcher.csvs import CsvReader, csv_writer


def test(sample_file: str) -> bool:
    # Test of the CsvReader class
    csv1 = CsvReader(sample_file, readHeader=False)
    # Test of the csv_writer function
    data = {1: [22, 33], 2: [77, 12], 4: [89, 32]}
    csv_writer('csv_writer_test.csv', data)
    return True


if __name__ == '__main__':
    test()
