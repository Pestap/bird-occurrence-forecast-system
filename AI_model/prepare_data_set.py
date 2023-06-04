import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import preprocessing

def load_from_file(filepath: str):
    df = pd.read_csv(filepath, sep=";")
    df['OBSERVATION COUNT'].replace({-100: 1}, inplace=True)
    print("Loaded from file")

    type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
             'OBSERVATION DATE': 'datetime64[s]', 'YEAR': int, 'WEEK OF YEAR': int, 'COUNTY': str, 'STATE': str}

    for col_name, type_name in type_dict.items():
        df[col_name] = df[col_name].astype(type_name)


    return df


def handle_same_place_same_time(df):

    df['MONTH'] = df.apply(lambda row: row['OBSERVATION DATE'].month, axis=1)

    for i in range(len(df)):
        if df.loc[i, 'OBSERVATION COUNT'] == -100:
            df.loc[i, 'OBSERVATION COUNT'] = average(df,df.loc[i, 'MONTH'], df.loc[i, 'YEAR'])

    df = df[['OBSERVATION COUNT', 'MONTH', 'YEAR', 'STATE']]
    df = df.groupby(['STATE', 'YEAR', 'MONTH'])['OBSERVATION COUNT'].mean().reset_index()
    print("Grouped")
    return df


def average(df, month, year):
    sum_year = 0
    count_year = 0

    sum_month = 0
    count_month = 0

    for i in range(len(df)):
        if df.loc[i, 'YEAR'] == year and df.loc[i, 'OBSERVATION_COUNT'] != -100:

            sum_year += df.loc[i, 'OBSERVATION COUNT']
            count_year += 1

            if df.loc[i, 'MONTH'] == month:
                sum_month += df.loc[i, 'OBSERVATION COUNT']
                count_month += 1

    if count_month != 0:
        return sum_month/count_month
    elif count_year != 0:
        return sum_year/count_year
    else:
        return 1


def divide_by_state(df):

    grouped = df.groupby(df.STATE)
    print(grouped)
    groups = []
    # ew. list comp
    for g in grouped.groups:
        groups.append(grouped.get_group(g))

    for group in groups:
        group.sort_values(['YEAR', 'MONTH'], ascending=[True, True], inplace=True)
        group.reset_index(inplace=True, drop=True)

    groups_with_zeroes = []
    # add zeroes
    for group in groups:
        year_months_dict = {}
        # get years and months present
        for i in range(len(group)):
            if group.loc[i, 'YEAR'] in year_months_dict:
                if not group.loc[i, 'MONTH'] in year_months_dict[group.loc[i, 'YEAR']]:
                    year_months_dict[group.loc[i, 'YEAR']].append(group.loc[i, 'MONTH'])
            else:
                year_months_dict[group.loc[i, 'YEAR']] = [group.loc[i, 'MONTH']]

        first_year = group.loc[0, 'YEAR']
        for i in range(first_year, 2023):
            if i in year_months_dict:
                # iterate through months
                for j in range(1,13):
                    if j not in year_months_dict[i]:
                        row = pd.DataFrame({'STATE': [group.loc[0, 'STATE']], 'YEAR': [i], 'MONTH': [j], 'OBSERVATION COUNT': [0.0]})
                        group = pd.concat([group, row], ignore_index=True)
                        #group.loc[len(group)] = {'STATE': group.loc[0, 'STATE'], 'YEAR': i, 'MONTH': j, 'OBSERVATION COUNT': 0}
            else:
                for j in range(1,13):
                    #group = group.append({'STATE': group.loc[0, 'STATE'], 'YEAR': i, 'MONTH': j, 'OBSERVATION COUNT': 0}, ignore_index=True)
                    row = pd.DataFrame(
                        {'STATE': [group.loc[0, 'STATE']], 'YEAR': [i], 'MONTH': [j], 'OBSERVATION COUNT': [0.0]})
                    group = pd.concat([group, row], ignore_index=True)
                    pass


        group.sort_values(['YEAR', 'MONTH'], ascending=[True, True], inplace=True)
        group.reset_index(inplace=True, drop=True)
        groups_with_zeroes.append(group)



    return groups_with_zeroes


def create_sets(test_size):

    #df = load_from_file('../data/ebd_PL_relJan-2023/ebd_PL_relJan-2023.txt')
    df = load_from_file('../data/ardea_alba.csv')
    df = handle_same_place_same_time(df)
    groups = divide_by_state(df)

    #model_x = groups[2]
    #df.sort_values(['YEAR', 'MONTH', 'WEEK'], ascending=[True, True], inplace=True)
    # target attribute
    y = df.iloc[:, 1]
    x = df.iloc[:, [2, 3, 5, 6]]

    x_numpy = x.values
    scaler = preprocessing.MinMaxScaler()
    x_s = scaler.fit_transform(x_numpy)
    x = pd.DataFrame(x_s)


    x_train, x_test, y_train, y_test = x.head(int(len(df.index)) - 1000), x.tail(1000),  y.head(int(len(df.index)) - 1000), y.tail(1000)

    return x_train, x_test, y_train, y_test



create_sets(0.2)