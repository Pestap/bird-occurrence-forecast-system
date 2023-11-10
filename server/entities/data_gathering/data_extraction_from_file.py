import pandas as pd
pd.options.mode.chained_assignment = None

def load_from_file(filepath: str):
    """
    Load data from created CSV file for give specie
    """
    df = pd.read_csv(filepath, sep=";")
    # -100 was set when extracting data from root file and replaced X
    df['OBSERVATION COUNT'].replace({-100: 1}, inplace=True)

    # type dictionary for casting types
    type_dict = {'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
             'OBSERVATION DATE': 'datetime64[D]', 'YEAR': int, 'WEEK OF YEAR': int, 'STATE': str}

    # cast types
    for col_name, type_name in type_dict.items():
        if col_name == 'OBSERVATION DATE':
            df[col_name] = pd.to_datetime(df[col_name], format="%d.%m.%Y")
            #df[col_name] = df[col_name].astype(type_name)
        else:
            df[col_name] = df[col_name].astype(type_name)

    return df


def handle_same_place_same_time(df):
    """
    Group observations by state, year and month
    """

    df['MONTH'] = df.apply(lambda row: row['OBSERVATION DATE'].month, axis=1)

    for i in range(len(df)): # TODO: for now never goes inside as -100 are replaced earlier
        if df.loc[i, 'OBSERVATION COUNT'] == -100:
            df.loc[i, 'OBSERVATION COUNT'] = average(df, df.loc[i, 'MONTH'], df.loc[i, 'YEAR'])

    df = df[['OBSERVATION COUNT', 'MONTH', 'YEAR', 'STATE']]
    df = df.groupby(['STATE', 'YEAR', 'MONTH'])['OBSERVATION COUNT'].mean().reset_index()
    return df


def get_columns_from_dataframe(df, column_list):
    return df[column_list]

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
                for j in range(1, 13):
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


def get_observations(filename):

    observations = load_from_file(filename)


    # group data
    df = handle_same_place_same_time(observations)
    groups = divide_by_state(df)

    group_tuples = []
    for group in groups:
        group_tuples.append((group.loc[0, 'STATE'], group))

    # handle observations
    observations = get_columns_from_dataframe(observations, ["OBSERVATION COUNT", "OBSERVATION DATE", "LATITUDE", "LONGITUDE"])


    return group_tuples, observations

