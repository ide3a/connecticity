# %% IMPORTS

import swmmio
import swmmio.utils.dataframes as swdf
import pandas as pd
import os
import re
import shutil
import plotly.graph_objects as go

import sys
sys.path.append("Challenge_Flood_the_SWMM/")
from paths import *
from src.utils.lid_data import lidNames


# %% FUNCTIONS

def get_node_df(node_id: str, rpt_dir: str) -> pd.DataFrame:
    """

    This function return the data that the SWMM simulation produced for the specified tank.

    :param tank_id: The ID of the Tank for which you want to get the data
    :param rpt_dir: The directory of the .rpt report file which you want to read the data from
    :return: The data collected during the simulation for the specified Tank as a DataFrame
    """
    section = 'Node Results'
    rpt_path = [os.path.join(rpt_dir, x) for x in os.listdir(rpt_dir) if x.endswith('.rpt')][0]
    res_node = swdf.dataframe_from_rpt(rpt_path, section, node_id)
    res_node.drop(res_node.tail(3).index, inplace=True)
    res_node.reset_index(inplace=True)
    res_node['Datetime'] = res_node['Date'] + ' ' + res_node['Time']
    res_node.drop(columns=['Date', 'Time'], inplace=True)
    for col in res_node.columns:
        try:
            res_node[col] = pd.to_numeric(res_node[col])
        except ValueError:
            try:
                res_node[col] = pd.to_datetime(res_node[col])
            except ValueError:
                continue
    return res_node


def plot_node_flooding_comparison(node_id: str, model_1_path: str, model_2_path: str, name_1: str,
                                name_2: str) -> go.Figure:
    """

    This function plots the inflow over time of the given tank for two different simulations results in order to compare
    the influence of different measures.

    :param tank_id: The ID of the tank whose data is to be plotted
    :param model_1_path: The path to the folder containing the .inp and .rpt files of the first model
    :param model_2_path: The path to the folder containing the .inp and .rpt files of the second model
    :param name_1: The name to give to the first trace to be plotted
    :param name_2: The name to give to the second trace to be plotted
    :return: The go.Figure() object to be further modified or plotted via .show()
    """
    node_data_model_1 = get_node_df(node_id, model_1_path)
    node_data_model_2 = get_node_df(node_id, model_2_path)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=node_data_model_1['Datetime'], y=node_data_model_1['FloodingCFS'],
                             name=name_1 + ' Flooding @ Node ' + node_id))
    fig.add_trace(go.Scatter(x=node_data_model_2['Datetime'], y=node_data_model_2['FloodingCFS'],
                             name=name_2 + ' Inflow @ Node ' + node_id))
    fig.update_yaxes(title_text='Node Flooding (m^3/s)')

    return fig


def produce_lid_setup_df(lid_type: str, area_ratio: float = 0.5, num_subcatchments: any = 'all', sort: str = 'd',
                         subcatchment_list: pd.Series = None, lid_usages: pd.DataFrame = None) -> pd.DataFrame:
    """

    This function produces a DataFrame of LID controls according to the specified lid_type. From the list of
    subcatchments in the model, the top X subcatchments are extracted, where X is the specified 'num_subcatchments'.
    The list of subcatchments can be sorted ascending or descending by area or randomly before this extraction via the
    parameter 'sort'. Alternatively a list of subcatchments can be explicitely specified via the parameter
    'subcatchment_list'. For each of the selected subcatchments, the ratio of area according to 'area_ratio' is set to
    be covered by the specified LID control. If you want to combine multiple LID controls, you can pass a previously
    created DataFrame of LID controls via the arguments 'lid_usages' to which the newly specified LID controls are
    appended.

    :param subcatchment_list: A list of subcatchments to apply the specified LID controls to. Arguments
    'num_subcatchments' and 'sort' will be ignored in this case.
    :param lid_type: The type of LID you want to apply. Types that can be used are specified in src.utils.lid_names
    :param area_ratio: The ratio of each of the subcatchments being covered by the LID control. (0 < area_ratio < 1)
    :param num_subcatchments: The number of subcatchments to apply the LID control to. This subcatchments will be taken
     from the top of the list of subcatchments in the model, which is sorted according to 'sort'
    :param sort: The way to sort the list of subcatchments by area. 'a' - ascending, 'd' - descending, 'r' - random
    :param lid_usages: The previously specified LID controls to append this new configuration to.
    :return: The LID controls as specified as a DataFrame to be written to a .inp file via
    src.utils.auxiliary_functions.write_lid_setup_to_inp
    """
    # inp_path = os.path.join(DATA_DIR, *['LID_setup_base', 'LID_setup_base.inp'])
    inp_path = os.path.join(DATA_DIR, *['baseline', 'Bellinge_2015_mod.inp'])
    model = swmmio.Model(inp_path)

    column_names = ['Subcatchment', 'LID Process', 'Number', 'Area', 'Width', 'InitSat', 'FromImp', 'ToPerv', 'RptFile',
                    'DrainTo', 'FromPerv']
    LID_params = ['SUB_NAME', 'LID_TYPE', 1, 'AREA', 0, 0, 0, 0, '*', '*', 0]
    if lid_type not in [getattr(lidNames, item) for item in dir(lidNames) if not item.startswith("__")]:
        raise BaseException('Invalid LID control name specified. Please only use ones from src.utils.lid_names.')
    LID_params[1] = lid_type

    lid_usages_for_inp = pd.DataFrame(data=[[x] for x in LID_params]).transpose()
    lid_usages_for_inp.columns = column_names

    subcatchments = model.subcatchments.dataframe

    if subcatchment_list is None:
        if num_subcatchments != 'all':
            if sort == 'd':
                subcatchments.sort_values(by='Area', inplace=True, ascending=False)
            elif sort == 'a':
                subcatchments.sort_values(by='Area', inplace=True, ascending=True)
            elif sort == 'r':
                subcatchments = subcatchments.sample(frac=1)
            else:
                raise BaseException(
                    'Invalid sort parameter name specified. Please only use a - ascending, d - descending, r - random.')

        if num_subcatchments == 'all':
            num_subcatchments = subcatchments.shape[0]
        elif int(num_subcatchments) <= subcatchments.shape[0]:
            num_subcatchments = int(num_subcatchments)
        else:
            raise BaseException(
                'Invalid number of subcatchments specified, can be *all* or any number smaller than the total number of '
                'subcatchments {}. Value specified was: {}'.format(subcatchments.shape[0], num_subcatchments))

        for id, subcatchment in subcatchments.head(num_subcatchments).iterrows():
            new_LID_vals = LID_params.copy()
            new_LID_vals[0] = id
            new_LID_vals[3] = 10000 * subcatchment['Area'] * area_ratio
            new_LID_vals = pd.DataFrame(data=new_LID_vals).transpose()
            new_LID_vals.columns = column_names
            lid_usages_for_inp = lid_usages_for_inp.append(new_LID_vals)
    else:
        subcatchment_list.drop_duplicates(inplace=True)
        for _, subcatchment in subcatchment_list.iteritems():
            new_LID_vals = LID_params.copy()
            new_LID_vals[0] = subcatchment
            new_LID_vals[3] = 10000 * subcatchments.loc[subcatchment]['Area'] * area_ratio
            new_LID_vals = pd.DataFrame(data=new_LID_vals).transpose()
            new_LID_vals.columns = column_names
            lid_usages_for_inp = lid_usages_for_inp.append(new_LID_vals)

    lid_usages_for_inp.reset_index(inplace=True, drop=True)
    lid_usages_for_inp.drop(index=0, inplace=True)

    if lid_usages is not None:
        tmp_area_check = lid_usages.copy()
        tmp_area_check = tmp_area_check.append(lid_usages_for_inp)
        tmp_area_check = tmp_area_check.groupby('Subcatchment')['Area'].sum()
        for id, subcatchment in subcatchments.iterrows():
            if id in tmp_area_check.index:
                if tmp_area_check[id] > 10000 * subcatchments.loc[id]['Area']:
                    raise BaseException('LID Controls on Subcatchment {} exceed the total area.'.format(id))
        return lid_usages.append(lid_usages_for_inp, ignore_index=True)
    else:
        return lid_usages_for_inp


def write_lid_setup_to_inp(lid_usages: pd.DataFrame, new_dir: str, new_filename: str, base_inp_dir: str = 'baseline',
                             base_inp_filename: str = 'Bellinge_2015_mod.inp') -> None:
    """

    This function produces a new .inp model file containing the specified LID Controls ('lid_usages'). The base .inp
    file is located under data/LID_setup_base. It is the standard Bellinge model containing the basic paramters for all
    LID controls. The new directory will be created of not already existent and afterwards contain the new .inp file
    with the specified name and the raindata file necessary for the execution of the simulation.

    :param lid_usages: The DataFrame containing the LID usages for the Subcatchments, as produced by the function
    src.utils.auxiliary_functions.produce_lid_setup_df
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

    insertion_txt = []
    for index, LID_usage in lid_usages.iterrows():
        insertion_txt.append(re.sub('\n\s*', '\t', LID_usage.to_string(header=False, index=False)).lstrip() + '\n')

    insertion_idx = inp_content.index('[LID_USAGE]\n') + 3
    del inp_content[insertion_idx]
    inp_content[insertion_idx:insertion_idx] = insertion_txt
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
