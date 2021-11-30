# %% IMPORTS
import os
import subprocess
from sys import platform
import re
import argparse

# %% FUNCTIONS

def run_external_program(cmd: list):
    p = subprocess.Popen(cmd, universal_newlines=True)
    p.communicate()


def run_swmm(path_to_inp: str, swmm_path: str):
    current_path = os.getcwd()
    inp_dir = os.path.dirname(path_to_inp)
    os.chdir(inp_dir)
    inp_file = os.path.basename(path_to_inp)
    reportfile = re.sub('.inp', '.rpt', inp_file)
    command = list()
    # if platform == 'linux' or platform == 'linux2' or platform == 'darwin':
    #     command.append('wine')
    command.append(swmm_path)
    command.append(path_to_inp)
    command.append(reportfile)
    run_external_program(command)
    os.chdir(current_path)


# %% MAIN

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--inp_path', type=str, required=True)
    parser.add_argument('--swmm_path', type=str, required=True)
    args = parser.parse_args()
    run_swmm(args.inp_path, args.swmm_path)
