# Overview of Contents

## Data folder
This folder is used to store all the swmm models used in your work. As a start, there's only the baseline Bellinge 
scenario, but all other modofied models you establish through the python notebook will be stored here by defauilt as 
well.

## Output folder
This folder can be used to store any output files you produce during your work. By default, some plots will be saved to 
this folder.

## Src folder
This folder contains all necessary code files. In the utils subfolder, there are some files with collections of 
functions you can use in the main notebook(s), as they already are in the provided one. In the main directory, there's 
two notebooks:

- `run_baseline`: contains code to test the setup and execute the simulation of the baseline model. Be sure to do this 
in the beginning because you will probably need the results of the baseline model later on.
- `main_script`: contains the most important functions you can use to alter LID controls in the scenario and 
demonstrates how to execute and analyze them. Further, there's some dummy code for a sensitivity analysis.