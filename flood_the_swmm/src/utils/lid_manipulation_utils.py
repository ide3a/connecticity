# %% IMPORTS

import sys
sys.path.append("Challenge_Flood_the_SWMM/")

from src.utils.lid_data import lidNames, lidParams, lidLayers, lidParamsPerLayer, lidLayersPerControl, lidParamStdValues
from paths import *

import os
import shutil


# %% LID CONTROL LISTS

lid_controls_long = [lidNames.bio_retention_cell, lidNames.green_roof, lidNames.permeable_pavement,
                     lidNames.rain_garden, lidNames.rain_barrel]
lid_controls_short = [lidNames.bio_retention_cell_short, lidNames.green_roof_short, lidNames.permeable_pavement_short,
                      lidNames.rain_garden_short, lidNames.rain_barrel_short]


# %% FUNCTIONS

def _get_val_from_str(name: str) -> any:
    res = None
    for lid_class in [lidNames, lidParams, lidParamsPerLayer, lidLayersPerControl, lidParamStdValues]:
        try:
            res = getattr(lid_class, name)
        except AttributeError:
            continue
    return res


def _make_default_dicts():
    all_lid_controls = dict()
    for lid_control_long, lid_control_short in zip(lid_controls_long, lid_controls_short):
        all_lid_controls[lid_control_long] = dict()
        for layer_name in _get_val_from_str(lid_control_long + lidLayers.layers_ext):
            cur_lid_dict = dict()
            [cur_lid_dict.update({layer_param: value}) for layer_param, value in
             zip(_get_val_from_str(layer_name + lidParamsPerLayer.layer_param_names_ext),
                 _get_val_from_str(layer_name + lidParamStdValues.param_defaults_ext + '_' + lid_control_short))]
            all_lid_controls[lid_control_long][layer_name] = cur_lid_dict
    return all_lid_controls


def _build_str_lid_control(lid_control: str, lid_control_data: dict) -> list:
    newline = '\n'
    tab = '\t'
    lid_start_line = lid_control + ' '
    lid = lid_start_line + _get_val_from_str(lid_control + '_short') + newline
    for layer in lid_control_data.keys():
        cur_line = lid_start_line + str(layer).upper()
        for param in lid_control_data[layer]:
            cur_line += tab + str(lid_control_data[layer][param])
        cur_line += newline
        lid += cur_line
    lid += newline
    return lid


def load_lid_dict() -> dict:
    """

    This function constructs and returns a dictionary with all parameters for all layers of all LID controls, i.e. the
    dictionary contains a sub-dictionary for each of the LID controls, which in turn contains a sub-dictionary for all
    layers of the respective LID control, which then contains a dictionary of all parameters of this specific layer.

    - LID Control 1
      - Layer 1
        - Parameter X
        - ...
    -   Layer 2
        - Parameter Y
        - ...
      - ...
    - LID Control 2
      - ...

    :return: the dict of all lid controls
    """
    return _make_default_dicts()


def write_lid_control_to_inp(lid_controls: dict, new_dir: str, new_filename: str, base_inp_dir: str = 'baseline',
                             base_inp_filename: str = 'Bellinge_2015_mod.inp') -> None:
    """

    This function produces a new .inp model file containing the specified LID Controls with the changed parameters.
    The new directory will be created inside the data directory of not already existent and afterwards contain the new .inp file
    with the specified name and the raindata file necessary for the execution of the simulation.


    :param lid_controls: The dict with the modified parameters of LID controls
    :param new_dir: The directory where the new files are to be saved
    :param new_filename: The filename of the newly created .inp file
    :param base_inp_dir: The directory where the .inp lies that is to be used as a base for the updates
    :param base_inp_filename: The filename of the base .inp file for the updates
    :return:
    """

    try:
        os.mkdir(new_dir)
    except FileExistsError:
        pass

    if not base_inp_filename.endswith('.inp'):
        base_inp_filename += '.inp'
    inp_path = os.path.join(DATA_DIR, *[base_inp_dir, base_inp_filename])
    with open(inp_path) as f:
        inp_content = f.readlines()
    f.close()

    all_lids = str()
    for lid_control_name in lid_controls.keys():
        all_lids += _build_str_lid_control(lid_control_name, lid_controls[lid_control_name])

    start_index = inp_content.index('[LID_CONTROLS]\n') + 3
    end_index = inp_content.index('[LID_USAGE]\n') - 1

    del inp_content[start_index:end_index]

    inp_content[start_index:start_index] = all_lids
    if not new_filename.endswith('.inp'):
        new_filename += '.inp'
    new_inp_path = os.path.join(new_dir, new_filename)

    with open(new_inp_path, 'w') as f:
        f.writelines(inp_content)
    f.close()

    rain_data_path_from = os.path.join(DATA_DIR, *['baseline', 'rg_bellinge_Apr2020.dat'])
    rain_data_path_to = os.path.join(new_dir, 'rg_bellinge_Apr2020.dat')
    shutil.copyfile(rain_data_path_from, rain_data_path_to)
    return
