from load_data import load_data
from prepare_data import prepare_data

col_list = ['SCIENTIFIC NAME', 'OBSERVATION COUNT', 'LATITUDE', 'LONGITUDE', 'OBSERVATION DATE']
type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float, 'OBSERVATION DATE': 'datetime64[s]'}

df = load_data(col_list, 'SCIENTIFIC NAME', 'Ardea alba')
df = prepare_data(df, type_dict)

print(df)