import string

import pandas as pd


def get_death_rate_for_states(file):
    """
    Get DataFrame including death rates for all states.
    The death rates are calculated on both genders and all age ranges.
    :param str file: Filename of death data
    :return: DataFrame including death rates with states as index
    :rtype: pd.DataFrame
    """
    data = pd.read_csv(file)
    data = data[data.gender == 'both']
    data = data[data.age == 'all']
    df = data.groupby('state')['d'].sum().to_frame()
    df['p'] = data.groupby('state')['p'].max().to_frame()

    # merge DC into Maryland and add state code
    df.loc["tmp"] = df.loc["Maryland"] + df.loc['D C']
    df.loc["Maryland"] = df.loc["tmp"]
    df['drate'] = df['d'] / df['p']
    df = df.drop(['D C'])
    df = df.drop(["tmp"])
    return df


def get_income_data(file):
    """
    Get income DataFrame from income data.
    :param str file: Filename of income data
    :return: Income DataFrame
    :rtype: pd.DataFrame
    """
    # read income data
    data = pd.read_csv(file)
    # remove useless parts
    data = data.iloc[5:57, 0:2]
    data.columns = ['state', 'Median HouseHold Income']
    data = data.reset_index()
    data = data.drop('index', axis=1)
    # remove comma
    for row in data.index:
        s = data['Median HouseHold Income'][row]
        s = float(s.translate(str.maketrans('', '', string.punctuation)))
        data['Median HouseHold Income'][row] = s
    # remove united states and D C to be in consistent with death data
    data = data.drop(0)
    data = data.drop(9)

    return data
