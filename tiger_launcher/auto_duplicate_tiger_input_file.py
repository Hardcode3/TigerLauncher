"""
FROM A SINGLE FILE, MULTIPLY IT BY THE NUMBER OF COMBINATIONS SPECIFIED BY THE USER
IN THE SETTINGS UNDER THE TIGER INPUT MODIFICATION SECTION
"""

import os

from settings import (
    permeaValues,
    faultThicknessValues,
    poroValues,
    compressibilityValues,
)
from tiger_launcher.misc_functions import (
    pythonLog,
    get_time
)


class AutoDuplicateTigerInputFile:
    """
    From a single TIGER input file, creates new ones using the settings (file in the root).
    These newly created files are named using a convention with @ symbols.
    """

    def __init__(self, tigerInputFile: str, log, verbose=False) -> None:
        self.verbose_: bool = verbose
        self.pylog_ = log
        pythonLog(
            self.pylog_,
            f"Class TigerInputMethod called\nTime : {get_time()}\nInput file to multiply : {tigerInputFile}\n",
            v=self.verbose_,
        )

        if isinstance(tigerInputFile, str) and os.path.exists(tigerInputFile):
            self.workingDir_: str = os.path.abspath("")
            self.output_path_: str = os.path.join(self.workingDir_, "../input")
            self.tiger_input_file: str = tigerInputFile
            for porosity in poroValues:
                for compressibility in compressibilityValues:
                    for permeability in permeaValues:
                        for faultThickness in faultThicknessValues:
                            self.duplicate_file(permeability, faultThickness, compressibility, porosity)
            pythonLog(
                self.pylog_,
                "--> Finished duplicating the input file\n",
                v=self.verbose_,
            )
        else:
            raise FileExistsError("The specified file does not exists")

    def duplicate_file(self,
                       new_fault_permeability: float,
                       new_fault_thickness: float,
                       new_fault_compressibility: float,
                       new_fault_porosity: float
                       ) -> None:
        """
        Duplicates the original file and modify the following parameters (some parameters can be easily added)
        :param new_fault_porosity: fault porosity (no unit)
        :param new_fault_compressibility: fault compressibility (in Pa-1)
        :param new_fault_permeability: fault permeability (in m2)
        :param new_fault_thickness: fault thickness (in m)
        """
        with open(self.tiger_input_file, "r") as file_in:
            new_file_name = f"{self.tiger_input_file.replace('.i', '')}@{new_fault_permeability}" \
                            f"@{new_fault_thickness}@{new_fault_compressibility}@{new_fault_porosity}@.i"
            pythonLog(self.pylog_, f"--> Created {new_file_name}\n", v=False)

            with open(new_file_name, "w") as fileOut:
                for line in file_in:
                    # to add possibilities, just use another elif statement to the following code and a marker on the
                    # file (here the markers are comments in uppercase that can not be found elsewhere in the file)
                    if "#FAULTPERMEA" in line:
                        fileOut.write(f"    k0 = {new_fault_permeability} #FAULTPERMEA\n")
                    elif "#FAULTTHICKNESS" in line:
                        fileOut.write(
                            f"    scale_factor = {new_fault_thickness} #FAULTTHICKNESS\n"
                        )
                    elif "#FAULTCOMPRESSIBILITY" in line:
                        fileOut.write(
                            f"    compressibility = {new_fault_compressibility} #FAULTCOMPRESSIBILITY\n"
                        )
                    elif "#FAULTPORO" in line:
                        fileOut.write(f"    porosity = {new_fault_porosity} #FAULTPORO\n")
                    elif "#OUTPUTNAME" in line:
                        new_file_name = f"  {line.strip().replace(' #OUTPUTNAME', '')}@{new_fault_permeability}@" \
                                        f"{new_fault_thickness}@{new_fault_compressibility}@{new_fault_porosity}@ " \
                                        f"#OUTPUTNAME\n"
                        fileOut.write(new_file_name)
                        # fileOut.write("solution_history = True\n")
                    else:
                        fileOut.write(line)
