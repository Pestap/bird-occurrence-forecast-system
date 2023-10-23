import sys

import pandas as pd


def get_name():
    return str(sys.argv[1]) if len(sys.argv) > 1 else None


def load_data_from_file(filepath="D:\\Piotrek\\inzynierka\\bird-occurence-forecast-system\\data\\ebd_PL_relJan-2023\\ebd_PL_relJan-2023.txt"):
    df = pd.read_csv(filepath, sep="\t")
    return df


def filter_by_specie_name(specie_name, df):
    filtered = df[df['COMMON NAME'] == specie_name]
    return filtered


def extract_columns(columns, df):
    return df[columns]


if __name__ == "__main__":
    df = load_data_from_file()
    columns = ['COMMON NAME', 'SCIENTIFIC NAME', 'OBSERVATION COUNT', 'COUNTRY', 'STATE CODE', 'STATE', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE']
    type_dict = {'COMMON NAME': str, 'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
                 'OBSERVATION DATE': 'datetime64[s]', 'STATE': str}
    spec_cols = extract_columns(columns, df)
    filtered = filter_by_specie_name("White Stork", df)


    print(filtered)

