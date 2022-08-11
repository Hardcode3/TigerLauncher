"""
This file contains the necessary class for reading CSV files (Csv_reader) and the function to create and write a new csv
file (csv_writer).
Both deals with dictionaries as containers.
"""

import csv
import os
from typing import Tuple


class CsvReader:
    """
    Open and extract data from a csv file based on its name.
    The data can then be used with python dictionaries containers.
    """
    separators = [',', ';', ' ']

    def __init__(self, fileName: str, separator=None, readHeader=False):
        self.fileName_ = fileName
        self.separator_ = separator
        self.readHeader_ = readHeader
        self.osSize_ = None
        self.cwd_ = None
        self.path_ = None
        self.reader_ = None
        self.header_ = None
        self.colNo_ = None
        self.size_ = 0
        self.data_ = {}

        self.open()

    # LAUNCH
    def open(self) -> None:
        """
        Opens the file and launch other methods to extract data in an automated way (controller).
        """
        if os.path.exists(self.fileName_):
            self.cwd_ = os.getcwd()
            self.path_ = os.path.realpath(self.fileName_)
            self.osSize_ = os.path.getsize(self.path_)
            self.reader_ = self.read()
            self.extract_data()
        else:
            raise FileNotFoundError(
                'The specified file or path does not exists')

    def read(self) -> None:
        """
        Read the csv file line by line using generators (memory efficiency).
        """
        for row in open(self.fileName_, 'r'):
            yield row

    def extract_data(self) -> None:
        """
        Extracts the data from the csv file.
        """
        firstLine = next(self.reader_)
        self.size_ = 1
        self.find_separator(firstLine)
        self.find_columns_number(firstLine)
        self.set_header(firstLine)
        for row in self.reader_:
            self.size_ += 1
            self.read_row(row)

    def read_row(self, row: str) -> None:
        """
        Splits a row (string type) into multiple strings to extract the real columns of the csv.
        """
        row = row.strip().split(self.separator_)
        for i in range(self.colNo_):
            self.data_[self.header_[i]].append(float(row[i]))

    def find_separator(self, line: str) -> str:
        """
        Finds the separator (string type) in a line and returns it.
        """
        for elt in CsvReader.separators:
            if elt in line:
                self.separator_ = elt
                return elt
        raise RuntimeError('No separator found')

    def set_header(self, line: str) -> None:
        """
        Set the header of the file if asked for.
        """
        if not self.readHeader_:
            self.header_ = [i for i in range(self.colNo_)]
            self.populate_data()
            self.read_row(line)
        else:
            self.header_ = [elt for elt in line.strip().split(self.separator_)]
            self.populate_data()

    def populate_data(self) -> None:
        """
        Writes the data from the csv file into the dictionary container.
        """
        for elt in self.header_:
            self.data_[elt] = []

    def find_columns_number(self, line: str) -> None:
        """
        Find the number of columns in the csv file.
        """
        if not self.separator_:
            self.find_separator(line)
        self.colNo_ = len(line.split(self.separator_))

    # PRINT
    def print(self, lowerIndex: int = -1, upperIndex: int = -1) -> None:
        """
        Prints the values taken from the csv file.
        Printed values can be sliced.
        :param lowerIndex: the lower slicer index
        :param upperIndex: the upper slicer index
        """
        if (lowerIndex < 0 or upperIndex <= 0) or not (isinstance(lowerIndex, int) and isinstance(upperIndex, int)) \
                or not (0 < lowerIndex < self.size_ - 1 and 1 < upperIndex < self.size_):
            lowerIndex = 0
            upperIndex = self.size_
        for key, values in self.data_.items():
            print(f"{key} :\n {values[lowerIndex:upperIndex]}")

    def print_sythesis(self) -> None:
        """
        Prints a synthesis of the extracted data.
        """
        print(
            f'\n{100 * "*"}')
        self.print_file_path()
        self.print_file_os_size()
        self.print_separator()
        self.print_column_number()
        self.print_size()
        self.print_header()
        print(
            f'{100 * "*"}\n')

    def print_data(self) -> None:
        """
        Prints the dictionary containing the extracted data.
        """
        print(f"  --> Data as dictionary :\n {self.data_}")

    def print_header(self) -> None:
        """
        Print the header of the csv file.
        """
        print(f"  --> Header as a list : {self.header_}")

    def print_size(self) -> None:
        """
        Print the number of rows in the csv file.
        """
        print(f"  --> File size (number of rows) : {self.size_}")

    def print_column_number(self) -> None:
        """
        Print the number of columns in th csv.
        """
        print(f"  --> Column number : {self.colNo_}")

    def print_separator(self) -> None:
        """
        Print the found separator.
        """
        print(f"  --> Separator : '{self.separator_}'")

    def print_file_path(self) -> None:
        """
        Print the path of the csv file file.
        """
        print(f"  --> File path : {self.path_}")

    def print_cwd(self) -> None:
        """
        Print the working directory (where the main file was executed).
        """
        print(f"  --> Current working directory : {self.fileName_}")

    def print_file_os_size(self) -> None:
        """
        Print the size (in bytes) of the csv file.
        :return:
        """
        print(f"  --> File size (os size) : {self.osSize_} bytes")

    """
    ACCESSORS
    """

    def get_array(self, colNo: int) -> Tuple[str, str]:
        """
        Gets a vector based on the column number (beginning with 0 index)
        :param colNo: the column number
        """
        if isinstance(colNo, int) and 0 <= colNo < self.colNo_:
            return self.header_[colNo], self.data_[self.header_[colNo]]
        raise RuntimeError(
            f'The column number should be an integer between 1 and {self.colNo_}')

    def get_data_size(self) -> int:
        """
        Gets the number of rows in the csv file.
        """
        return self.size_

    def get_header(self) -> list:
        """
        Gets the complete header extracted from the csv file, or default header when read_header is False.
        """
        return self.header_

    def get_cwd(self) -> str:
        """
        Gets the current working directory.
        """
        return self.cwd_

    def get_path(self) -> str:
        """
        Gets the path of the csv file.
        """
        return self.path_

    def get_data(self) -> dict:
        """
        Gets the dictionary containing the data of the csv file.
        """
        return self.data_

    def get_column_number(self) -> int:
        """
        Gets the number of columns in the csv file.
        """
        return self.colNo_

    def get_separator(self) -> str:
        """
        Gets the seperator of the csv file.
        """
        return self.separator_

    def os_file_size(self) -> int:
        """
        Gets the os file size in bytes.
        """
        return self.osSize_


def csv_writer(file_name: str, data: dict) -> CsvReader:
    """
    Writes a csv from a specified name and data, presented using a dictionary.
    :param file_name: the name of the csv file that must be created
    :param data: the dictionary containing data (values) and the header (keys)
    :return a CsvReader entity, already processed.
    """
    if isinstance(file_name, str) and isinstance(data, dict):
        with open(file_name, 'w') as csvF:
            writer = csv.writer(csvF)
            header = [elt for elt in data.keys()]
            writer.writerow(header)
            length = len(data[header[0]])
            for i in range(length):
                row = []
                for elt in header:
                    row.append(data[elt][i])
                writer.writerow(row)
    return CsvReader(file_name, readHeader=True)

