"""
This file automates the launch of TIGER in the terminal for input files located in the input directory.
Uses the dependencies under tiger_launcher to run.
Print logs into the logs' folder for python console and terminal (error troubleshooting).
Outputs every file in the output folder.
"""
import _io
import multiprocessing
import os
import subprocess
import time
from typing import Tuple

from settings import (
    excludedCSV,
    excludedExodus,
    excludedInput,
    TIGER_PATH,
    WORKING_DIRECTORY
)
from tiger_launcher.misc_functions import (
    pythonLog,
    get_time
)


def set_core_number(core_number: int = None) -> int:
    """
    Return the processor core number (logical and physical) if the input is possible. Otherwise, prints an error
    message and set the number of processor cores to 1
    :param core_number: the number of physical and logical processor cores
    """
    if core_number is None:
        return multiprocessing.cpu_count()
    elif isinstance(core_number, int) and 1 <= core_number < multiprocessing.cpu_count():
        return core_number
    else:
        print("The specified core number is incorrect, the machine can not run the code")
        return 1


class AutoTigerLaunch:
    """
    Launch TIGER automatically on every input file present in the input directory.
    """

    def __init__(self, log: _io.TextIOWrapper, core_number: int = None, verbose: bool = False) -> None:

        if isinstance(TIGER_PATH, str) and os.path.exists(TIGER_PATH):
            self.view_ = AutoTigerLaunchView(log, verbose)
            self.cwd_: str = WORKING_DIRECTORY
            self.input_directory_: str = os.path.join(WORKING_DIRECTORY, "input")
            self.output_dir_: str = os.path.join(WORKING_DIRECTORY, "output")
            self.logs_dir_: str = os.path.join(WORKING_DIRECTORY, "logs")
            self.input_file_list_: list = []
            self.csv_file_list_: list = []
            self.exodus_file_list_: list = []
            self.input_file_number_: int = 0
            self.csv_file_number_: int = 0
            self.exodus_file_number_: int = 0
            self.core_number_: int = set_core_number(core_number)
            self.success_ = None

            self.view_.class_called()
            self.view_.current_working_directory(self.cwd_)
            self.view_.infos_before_launch(WORKING_DIRECTORY, TIGER_PATH, self.core_number_)
            # EXECUTION
            self.run_input_files_in_terminal()
        else:
            raise FileNotFoundError(f"The path of TIGER {TIGER_PATH} is not correct")

    def find_input_files(self, search_path: str, additional_selector=None) -> Tuple[list, list, list]:
        """
        Finds the files in the considered directory (input files .i, csv files .csv and exodus files).
        :param search_path: the path (relative) where the function should be searching
        :param additional_selector: a selector to restrict the search
        :return: a tuple of len 3 containing the name's list for every file type (input, csv, exodus)
        """
        if os.path.exists(os.path.join(self.cwd_, search_path)):
            search_path = os.path.join(self.cwd_, search_path)
        else:
            self.view_.absolute_search_path(self.cwd_, search_path)
            raise FileNotFoundError("The path does not exist")

        if not additional_selector:
            additional_selector = ""
            self.view_.find_files_in_path(search_path)

        for file in os.listdir(search_path):
            if file.endswith(".i") and file not in excludedInput:
                if additional_selector in file:
                    self.input_file_list_.append(file)
            elif file.endswith(".csv") and file not in excludedCSV:
                if additional_selector in file:
                    self.csv_file_list_.append(file)
            elif file.endswith(".e") and file not in excludedExodus:
                if additional_selector in file:
                    self.exodus_file_list_.append(file)

        self.input_file_number_: int = len(self.input_file_list_)
        self.csv_file_number_: int = len(self.csv_file_list_)
        self.exodus_file_number_: int = len(self.exodus_file_list_)

        if self.input_file_number_ == 0 and self.csv_file_number_ == 0 and self.exodus_file_number_:
            raise FileExistsError(
                "Reconsider the file path of the input files, there is no files inside or the path is incorrect"
            )

        self.view_.found_input_files_infos(self.input_file_list_, self.csv_file_list_, self.exodus_file_list_)
        return self.input_file_list_, self.csv_file_list_, self.exodus_file_list_

    def run_input_files_in_terminal(self) -> None:
        """
        Run the input files from the input root directory in the terminal using TIGER.
        """
        self.view_.run_tiger_in_terminal()
        fileName: str = f"{self.logs_dir_}/log_{get_time()}.txt"

        with open(fileName, "w") as text_file_output:
            count: int = 0
            input_file_list, _, _ = self.find_input_files(self.input_directory_)
            for file_path in input_file_list:
                start_time = time.time()
                count += 1
                self.view_.running_tiger_infos(count, self.input_file_number_, time.time() - start_time, file_path)
                launch_tiger_command = \
                    f"mpirun -n {self.core_number_} {TIGER_PATH} -i " \
                    f"{os.path.join(self.input_directory_, file_path)}"
                last_launch_time = time.time()
                process = subprocess.run(['mpirun', '-n', str(self.core_number_), TIGER_PATH, '-i',
                                          os.path.join(self.input_directory_, file_path)],
                                         capture_output=True, text=True)
                if process.returncode != 0:
                    self.success_ = False
                    text_file_output.write(
                        "ERROR\n"
                        f"Return code : {process.returncode}\n"
                        f"Process : {process.stdout}\n"
                        f"Error : {process.stderr}\n")
                    raise RuntimeError("There was an error during the process, check the log folder to learn more")
                text_file_output.write(
                    f"{100 * '*'}\n"
                    f"{100 * '*'}\n"
                    f"{get_time()}"
                    f"EXECUTING TIGER:\n"
                    f"File path : {file_path}\n"
                    f"Currently executed file : {file_path}\n"
                    f"Number of used cores : {self.core_number_}\n"
                    f"Path of the tiger executable : {TIGER_PATH}\n"
                    f"Command line run : {launch_tiger_command}\n"
                    f"Executed in {round(time.time() - start_time, 2)} seconds\n"
                    f"Exit code : {process.returncode}\n"
                    f"Eventual errors : {process.stderr}\n"
                    f"Output :\n {process.stdout}\n\n"
                    f"{100 * '*'}\n"
                    f"{100 * '*'}\n\n"
                )
                self.view_.file_processed(file_path, time.time() - last_launch_time)
                self.view_.finished_running_input_files(count)
        self.success_ = True

    @property
    def success(self) -> bool:
        """
        Gets the boolean corresponding to the success of the simulation set.
        """
        return self.success_
        
    def get_input_files(self) -> list:
        """
        Gets input file's list from the search directory.
        """
        return self.input_file_list_

    def get_csv_files(self) -> list:
        """
        Gets csv file's list from the search directory.
        """
        return self.csv_file_list_

    def get_exodus_files(self) -> list:
        """
        Gets exodus file's list from the search directory.
        """
        return self.exodus_file_list_

    def get_used_processor_cores(self) -> int:
        """
        Gets the selected cpu cores for the simulations.
        """
        return self.core_number_

    def get_input_file_count(self) -> int:
        """
        Gets the number of input files detected in the search path.
        """
        return self.input_file_number_

    def get_csv_file_count(self) -> int:
        """
        Gets the number of csv files detected in the search path.
        """
        return self.csv_file_number_

    def get_exodus_file_count(self) -> int:
        """
        Gets the number of exodus files detected in the search path.
        """
        return self.exodus_file_number_


class AutoTigerLaunchView:
    """
    This class is the view for the AutoTigerLaunch class (model).
    """

    def __init__(self, log: _io.TextIOWrapper, verbose: bool):
        if isinstance(log, _io.TextIOWrapper) and isinstance(verbose, bool):
            self.pylog_ = log
            self.verbose_ = verbose
        else:
            raise RuntimeError(f"The instance passed to the AutoTigerLaunchView has an unexpected type {type(log)}")

    def class_called(self) -> None:
        """
        Prints and log that the AutoTigerLaunch class was called.
        """
        pythonLog(self.pylog_, "\nAutoTigerLaunch class called\n", v=self.verbose_)

    def current_working_directory(self, cwd: str) -> None:
        """
        Prints and log the working directory associated to the project.
        """
        pythonLog(self.pylog_, f"--> Working directory : {cwd}\n", v=self.verbose_)

    def infos_before_launch(self, cwd: str, tiger_path: str, core_number: int) -> None:
        """
        Prints and log basic data before the launch of the simulation: path and parameters.
        """
        pythonLog(
            self.pylog_,
            f"--> Path of the folder containing the input files for the TIGER simulation : \n"
            f"  {os.path.join(cwd, '../input')}\n"
            f"--> Path of the tiger-opt executable : {tiger_path}\n"
            f"--> Number of cores / threads used for the simulation : {core_number}\n"
            f"--> Execution is about to begin\n",
            v=self.verbose_)

    def absolute_search_path(self, cwd: str, search_path: str) -> None:
        """
        Prints and log the search path (to further detect the input files)
        """
        pythonLog(self.pylog_, f"--> Issue : {os.path.join(cwd, search_path)}\n", v=self.verbose_)

    def find_files_in_path(self, search_path: str) -> None:
        """
        Prints and log that AutoTigerLauncher class is discovering files in path.
        """
        pythonLog(self.pylog_, f"--> Finding files in path : {search_path}...\n", v=self.verbose_)

    def found_input_files_infos(self, input_file_list: list, csv_file_list: list, exodus_file_list: list) -> None:
        """
        Prints and log the found files in the search path.
        """
        pythonLog(
            self.pylog_,
            f"\n{100 * '*'}\n"
            f"    Input files ({len(input_file_list)}):\n{input_file_list}\n\n"
            f"    CSV files ({len(csv_file_list)}):\n{csv_file_list}\n\n"
            f"    Exodus files ({len(exodus_file_list)}):\n{exodus_file_list}\n\n"
            f"{100 * '*'}\n",
            v=False)

    def run_tiger_in_terminal(self):
        """
        Prints and log that AutoTigerLauncher is running TIGER through the terminal.
        """
        pythonLog(self.pylog_, "--> Running TIGER through the terminal ...\n", v=self.verbose_)

    def running_tiger_infos(self, count: int, input_file_count: int, elapsed_time: float, current_running_file: str) \
            -> None:
        """
        Prints and log various information for the simulations (while TIGER is running).
        """
        pythonLog(
            self.pylog_,
            f"--> LOOP: {count} / {input_file_count}\n"
            f"--> Elapsed since beginning: {elapsed_time}\n"
            f"--> Currently running: {current_running_file} ...\n",
            v=self.verbose_)

    def file_processed(self, current_file_path: str, elapsed_time: float) -> None:
        """
        Prints and log that all files were processed.
        """
        pythonLog(
            self.pylog_,
            f"--> Input file {current_file_path} processed in {elapsed_time}, switching to the next one ...\n",
            v=self.verbose_)

    def finished_running_input_files(self, file_count: int):
        """
        Prints and log a finish message.
        """
        pythonLog(self.pylog_, f"--> TIGER finished computing {file_count} input files\n", v=self.verbose_)
