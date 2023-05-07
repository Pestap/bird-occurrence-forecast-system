from load_data import load_data
from prepare_data import prepare_data

from sklearn.model_selection import train_test_split


def create_sets(test_size):
    col_list = ['SCIENTIFIC NAME', 'OBSERVATION COUNT', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE']
    type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
                 'OBSERVATION DATE': 'datetime64[s]'}

    df = load_data(col_list, 'SCIENTIFIC NAME', 'Ardea alba')
    df = prepare_data(df, type_dict)

    # target attribute
    y = df.iloc[:, 1]
    x = df.iloc[:, [2, 3, 5, 6]]

    x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=100, test_size=test_size, shuffle=True)

    return x_train, x_test, y_train, y_test


