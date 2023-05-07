import pandas as pd

from load_data import load_data


def handle_missing_value(df, column_name):
    df[column_name].replace({'X': 1}, inplace=True)
    return df


def parse_datatypes(df, type_dict):
    for col_name, type_name in type_dict.items():
        df[col_name] = df[col_name].astype(type_name)
    return df


def parse_dates(df):
    df['YEAR'] = df.apply(lambda row: row['OBSERVATION DATE'].year, axis=1)
    df['WEEK OF YEAR'] = df.apply(lambda row: row['OBSERVATION DATE'].isocalendar().week, axis=1)
    return df


def prepare_data(df, type_dict):

    df = handle_missing_value(df, 'OBSERVATION COUNT')
    df = parse_datatypes(df, type_dict)
    df = parse_dates(df)

    return df
