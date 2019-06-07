import sqlite3
from os import walk

import numpy as np
import pandas as pd
from pandas.io import sql


def merge_data(states_path, population_file, output):
    """
    Merge scrapped data and generate a big .csv file as the main dataset for this project.
        - add gender and state columns
        - add death rates for each age range
        - change ages to one column
    :param str states_path: Directory that contain scrapped death data
    :param str population_file: Filename of scrapped population data
    :param str output: Filename of output .csv file
    :return: None
    :rtype: None
    """
    # # Merge data files by adding gender and state columns
    # read the data
    f = []

    # get all filenames in the directory
    for (a, b, filenames) in walk(states_path):
        f.extend(filenames)

    # split the filenames
    data_contain = {'name': [], 'd_all': [], 'd_0_14': [], 'd_15_24': [], 'd_25_34': [], 'd_35_44': [],
                    'd_45_54': [], 'd_55_64': [],
                    'd_65_74': [], 'd_75+': [], 'gender': [], 'state': []}

    all_data = pd.DataFrame(data_contain)
    # read the data sheet
    gender = ['female', 'male', 'both']

    # add the population to the file, population= dict type
    population = {}

    for g in gender:
        population[g] = pd.read_excel(population_file, sheet_name=g)
        population[g].set_index("state", drop=True, append=False, inplace=True)

    for filename in f:
        if filename.split(".")[0] == '':
            continue
        path = states_path + filename

        # read the state data
        for g in gender:
            state_name = filename.split(".")[0]  # generate state name by using filename {statename.xlsx}
            state_data = pd.read_excel(path, sheet_name=g)  # read state data
            disease_number = state_data.shape[0]  # the row number for this state data = the number of the disease
            state_data['gender'] = [g] * disease_number
            state_data['state'] = [state_name] * disease_number

            state_population = pd.DataFrame(
                np.repeat((population[g].loc[[state_name], :]).values, disease_number,
                          axis=0))  # read the population data
            state_population.columns = population[g].columns
            state_data = state_data.join(state_population)  # join state_data with population data

            all_data = all_data.append(state_data, ignore_index=True, sort=False)

    # # Calculate death rates for each age range

    # calculate death rate
    ranges = np.array([0] + [(5 + 10 * x) for x in range(1, 8)])  # [ 0, 15, 25, 35, 45, 55, 65, 75]
    ranges = np.hstack((ranges[:, None], (ranges + 10 * np.ones(len(ranges)))[:, None]))
    ranges[0, 1] = ranges[1, 0]
    ranges[-1, -1] = -1
    all_data['drate_all'] = all_data['d_all'] / all_data['p_all']
    for rg in ranges:
        s, e = [int(i) for i in rg.tolist()]
        if e > 0:
            age_range = f"{s}_{e - 1}"
        else:
            age_range = f"{s}+"
        all_data['drate_' + age_range] = all_data['d_' + age_range] / all_data['p_' + age_range]

    # # Change ages to one column

    # load data into db
    conn = sqlite3.connect(':memory:')
    all_data.to_sql('Table1', conn)

    frames = []
    age_range = "all"
    query = f"select name,\"d_{age_range}\" as d,\"p_{age_range}\" as p,\"drate_{age_range}\" as drate,state,gender from Table1;"
    # print(query)
    df = sql.read_sql_query(query, conn)
    row_number = df.shape[0]
    df['age'] = [age_range] * row_number
    frames.append(df)
    for rg in ranges:
        s, e = [int(i) for i in rg.tolist()]
        if e > 0:
            age_range = f"{s}_{e - 1}"
        else:
            age_range = f"{s}+"
        query = f"select name,\"d_{age_range}\" as d,\"p_{age_range}\" as p,\"drate_{age_range}\" as drate,state,gender from Table1;"
        # print(query)
        df = sql.read_sql_query(query, conn)
        row_number = df.shape[0]
        df['age'] = [age_range] * row_number
        frames.append(df)
    all_data_ages = pd.concat(frames)

    all_data_ages.to_csv(output, index=False)
