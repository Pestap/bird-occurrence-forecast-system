from geopy.geocoders import Nominatim


# handle missing values (replace invalid with -100, will be dropped later if needed)
def handle_missing_values(df, column_name):
    df[column_name].replace({'X': -100}, inplace=True)
    print("Handled missing values")
    return df


# parse datatypes according to provided dictionary
def parse_datatypes(df, type_dict):
    for col_name, type_name in type_dict.items():
        df[col_name] = df[col_name].astype(type_name)
    print("Parsed datatypes")
    return df


# parse dates - get year and week of year
def parse_dates(df):
    df['YEAR'] = df.apply(lambda row: row['OBSERVATION DATE'].year, axis=1)
    df['WEEK OF YEAR'] = df.apply(lambda row: row['OBSERVATION DATE'].isocalendar().week, axis=1)
    print("Parsed dates")
    return df


# get counties and states for all observations
def reverse_geocoding(df):
    geolocator = Nominatim(user_agent="coords_powiaty_and_woj")

    def get_county_and_state(row):

        county = 'unknown'
        state = 'unknown'
        try:
            result = geolocator.reverse(str(row['LATITUDE']) + "," + str(row['LONGITUDE'])).raw['address']
            county = result['county']
            state = result['state']
        except:
            try:
                result = geolocator.reverse(str(row['LATITUDE']) + "," + str(row['LONGITUDE'])).raw['address']
                county = result['city']
                state = result['state']
            except:
                if county == 'unknown':
                    county = 'no_county'
                if state == 'unknown':
                    state = 'no_state'
        return {'COUNTY': county, 'STATE': state}

    print("Began reverse geocoding")
    df[['COUNTY', 'STATE']] = df.apply(lambda row: get_county_and_state(row), axis=1, result_type='expand')
    df = df[df['COUNTY'] != 'no_county']
    df = df[df['STATE'] != 'no_state']
    print("Finished reverse geocoding")
    return df


# for the whole process for data preperation
def prepare_data(df, type_dict={'SCIENTIFIC NAME': str, 'OBSERVATION COUNT': int, 'LATITUDE': float, 'LONGITUDE': float,
             'OBSERVATION DATE': 'datetime64[s]'}):

    df = handle_missing_values(df, 'OBSERVATION COUNT')
    df = parse_datatypes(df, type_dict)
    df = parse_dates(df)
    df = reverse_geocoding(df)

    return df
