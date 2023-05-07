from geopy.geocoders import Nominatim


def handle_missing_value(df, column_name):
    df[column_name].replace({'X': 1}, inplace=True)
    print("Handled missing values")
    return df


def parse_datatypes(df, type_dict):
    for col_name, type_name in type_dict.items():
        df[col_name] = df[col_name].astype(type_name)
    print("Parsed datatypes")
    return df


def parse_dates(df):
    df['YEAR'] = df.apply(lambda row: row['OBSERVATION DATE'].year, axis=1)
    df['WEEK OF YEAR'] = df.apply(lambda row: row['OBSERVATION DATE'].isocalendar().week, axis=1)
    print("Parsed dates")
    return df


def reverse_geocoding(df):
    geolocator = Nominatim(user_agent="coords_powiaty")
    def get_county(row):

        county = 'unknown'
        try:
            county = geolocator.reverse(str(row['LATITUDE']) + "," + str(row['LONGITUDE'])).raw['address']['county']
            print(county)
        except:
            print("EIEHOEE")
            try:
                county = geolocator.reverse(str(row['LATITUDE']) + "," + str(row['LONGITUDE'])).raw['address']['city']
            except:
                county = 'no_county'

        return county

    print("Began reverse geocoding")
    df['COUNTY'] = df.apply(lambda row: get_county(row), axis=1)
    df = df[df['COUNTY'] != 'no_county']
    print("Finished reverse geocoding")
    return df


def prepare_data(df, type_dict):

    df = handle_missing_value(df, 'OBSERVATION COUNT')
    df = parse_datatypes(df, type_dict)
    df = parse_dates(df)
    df = reverse_geocoding(df)

    return df
