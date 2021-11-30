import os

# BASE PATH
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


# folder containing .mat files (output from STREaM)
MAT_DIR = os.path.join(ROOT_DIR, 'mat')

# data folder with water enduse data
DATA_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'data')

# result folder
RESULT_DIR = os.path.join(os.path.dirname(ROOT_DIR), 'results')