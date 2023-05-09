from load_data import load_data
from prepare_data import prepare_data
import matplotlib.pyplot as plt


# save extracted data to file
def save_df_to_file(df, path='../data/tests/test.csv'):
    df.to_csv(path, sep=';', encoding='utf-8', index=False)
    print("Saved to: " + path)


def plot(df, x_axis_name='OBSERVATION DATE', y_axis_name='OBSERVATION COUNT'):
    x_axis = df.loc[:, x_axis_name]
    y_axis = df.loc[:, y_axis_name]

    plt.plot(x_axis, y_axis, 'o')
    plt.xlabel(x_axis_name)
    plt.ylabel(y_axis_name)

    plt.grid(True)
    plt.show()
    print("plot")


col_list = ['SCIENTIFIC NAME', 'OBSERVATION COUNT', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE']
type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
             'OBSERVATION DATE': 'datetime64[s]'}

df = load_data(col_list, 'SCIENTIFIC NAME', 'Ardea alba', filepath='../data/ebd_PL_relJan-2023/test.txt')
df = prepare_data(df, type_dict)

plot(df)
save_df_to_file(df) #,'../data/ardea_alba.csv')




