"""
SETTINGS FILE
"""
from tiger_launcher.external.get_project_root.get_project_root.get_project_root import root_path

WORKING_DIRECTORY: str = root_path(ignore_cwd=True)
TIGER_PATH = '/home/baptiste/projects/tiger/tiger-opt'

# VALUES USED BY KONRAD ET AL, 2016
# from Konrad et al : fault storage : 1.6e-10 1.12e-10 5.2e-11 2e-12
# from Konrad et al : fault thickess : 50, 150
# from Konrad et al : fault permea : 1e-14 1e-9


# SETTINGS (FAULT PARAMETERS ONLY)

# select the ranges of values for each parameter
# note that the simulation can be long and varying two parameters can produce a lot of input files
permeaValues = [1e-10, 1e-11, 1e-12, 1e-13, 1e-14, 1e-15]
faultThicknessValues = [0.01, 0.05, 0.1, 0.2, 0.5, 1]
poroValues = [0.2]
compressibilityValues = [5e-10]


# SETTINGS FOR THE AUTOTIGER CLASS

# the list of input files that wont be analyzed
excludedInput = [
    "Pullach_TH_220506_TH3cal_short.i",
    "Pullach_TH_220506_TH3cal_long.i",
    "Pullach_TH_220506_TH2cal_short.i",
    "Pullach_TH_220506_TH3cal_long_pump_time.i",
]

# the list of csv that wont be analyzed
excludedCSV = [
    "KZPV1_Gesamt_PULL1a_tQ.csv",
    "KZPV1_Gesamt_PULL2_2005_tQ.csv",
    "KZPV_TH3_2011_tQ _long_pumping_time.csv",
]

# the list of exodus that wont be analyzed
excludedExodus = ["220413_bhfw_apsmf2.e"]

# the path of tha experimental data (csv)
TH1Path = "KZPV1_TH1a_p_experiment.csv"
TH2Path = "KZPV_TH2_p_experiment.csv"
TH3Path = "KZPV_TH3_2011_tP_experiment.csv"
