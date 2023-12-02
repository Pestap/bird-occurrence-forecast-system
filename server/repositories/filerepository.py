import pandas as pd

from repositories.data_processing import process_observations


def load_from_file(filepath: str):
    """
    Load data from created CSV file for give specie
    """
    df = pd.read_csv(filepath, sep=";")
    # -100 was set when extracting data from root file and replaced X
    df['OBSERVATION COUNT'].replace({-100: 1}, inplace=True)

    # type dictionary for casting types
    type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
             'OBSERVATION DATE': 'datetime64[D]', 'YEAR': int, 'WEEK OF YEAR': int, 'STATE': str}

    # cast types
    for col_name, type_name in type_dict.items():
        if col_name == 'OBSERVATION DATE':
            df[col_name] = pd.to_datetime(df[col_name], format="%d.%m.%Y")
        else:
            df[col_name] = df[col_name].astype(type_name)

    return df


def get_observations(filename):
    observations = load_from_file(filename) # for loading from file
    return process_observations(observations)

