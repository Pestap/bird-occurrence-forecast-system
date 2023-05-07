from load_data import load_data
from prepare_data import prepare_data

def save_df_to_file(df, path='../data/test.csv'):
    df.to_csv(path, sep=';', encoding='utf-8', index=False)
    print("Saved to: " + path)


col_list = ['SCIENTIFIC NAME', 'OBSERVATION COUNT', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE']
type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
             'OBSERVATION DATE': 'datetime64[s]'}

df = load_data(col_list, 'SCIENTIFIC NAME', 'Ardea alba', filepath='../data/ebd_PL_relJan-2023/test.txt')

df = prepare_data(df, type_dict)

save_df_to_file(df)




