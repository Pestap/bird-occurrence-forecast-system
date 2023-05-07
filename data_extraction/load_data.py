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



df = load_from_file('../data/ebd_PL_relJan-2023/ebd_PL_relJan-2023.txt')
df2 = extract_rows_by_column_value(df, 'SCIENTIFIC NAME', 'Ardea alba')

print(df2)
input()