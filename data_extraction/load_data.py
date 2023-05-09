import pandas as pd


# Loads data from file (eBird file)
def load_from_file(filepath: str):
    df = pd.read_csv(filepath, sep="\t", dtype=str)
    return df


# Extract the columns needed
def extract_columns(df, column_names=['SCIENTIFIC NAME', 'OBSERVATION COUNT', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE']):
    # extract the columns specified in the list
    df = df[column_names]
    return df


# extract the rows needed, filtering by specified column name
def extract_rows_by_column_value(df, column_name: str, column_value: str):

    # get only the needed rows
    df = df[df[column_name] == column_value]

    return df


# Function for the whole process of loading and extracting needed data
def load_data(columns_to_extract, filter_column_name, filter_column_value,
              filepath='../data/ebd_PL_relJan-2023/ebd_PL_relJan-2023.txt'):
    df = load_from_file(filepath)
    df = extract_rows_by_column_value(df, filter_column_name, filter_column_value)
    df= extract_columns(df, columns_to_extract)
    print("Loaded data")
    return df

