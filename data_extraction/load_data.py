import pandas as pd


def load_from_file(filepath: str):
    df = pd.read_csv(filepath, sep="\t", dtype=str)
    return df


def extract_columns(df, column_names):
    df_only_cols_from_list = df[column_names]
    return df_only_cols_from_list


def extract_rows_by_column_value(df, column_name: str, column_value: str):

    df_species_rows = df[df[column_name] == column_value]

    return df_species_rows


def load_data(columns_to_extract, filter_column_name, filter_column_value, filepath='../data/ebd_PL_relJan-2023/ebd_PL_relJan-2023.txt'):
    df = load_from_file(filepath)
    df_needed_rows = extract_rows_by_column_value(df, filter_column_name, filter_column_value)
    df_needed_cols = extract_columns(df_needed_rows, columns_to_extract)

    return df_needed_cols

