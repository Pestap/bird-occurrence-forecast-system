import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def load_from_file(filepath: str):
    df = pd.read_csv(filepath, sep=";")
    print("Loaded from file")
    return df


def handle_same_place_same_time(df):
    df = df[['OBSERVATION COUNT', 'WEEK OF YEAR', 'YEAR', 'COUNTY']]


    df = df.groupby(['COUNTY', 'YEAR', 'WEEK OF YEAR'])['OBSERVATION COUNT'].mean().reset_index()
    print("Grouped")
    return df

def divide_by_county(df):

    grouped = df.groupby(df.COUNTY)
    print(grouped)
    groups = []
    # ew. list comp
    for g in grouped.groups:
        groups.append(grouped.get_group(g))

    for group in groups:
        group.sort_values(['YEAR', 'WEEK OF YEAR'], ascending=[True, True], inplace=True)


    return groups


def create_sets(test_size):

    #df = load_from_file('../data/ebd_PL_relJan-2023/ebd_PL_relJan-2023.txt')
    df = load_from_file('../data/ardea_alba.csv')
    df = handle_same_place_same_time(df)
    groups = divide_by_county(df)

    model_x = groups[2]

    # target attribute
    y = df.iloc[:, 1]
    x = df.iloc[:, [2, 3, 5, 6]]

    x_numpy = x.values
    scaler = preprocessing.MinMaxScaler()
    x_s = scaler.fit_transform(x_numpy)
    x = pd.DataFrame(x_s)


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size, shuffle=True)

    return x_train, x_test, y_train, y_test



create_sets(0.2)