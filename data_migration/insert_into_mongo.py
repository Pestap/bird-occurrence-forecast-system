import csv
import os
from datetime import datetime
from pymongo import MongoClient

username = "bird_app"
password = "Czapla#123"

host = "localhost"
port = 27017
database_name = "bird_occurrence_forecast_system"
collection_name = "observation_data"

mongo_uri = f"mongodb://{username}:{password}@{host}:{port}/{database_name}"
client = MongoClient(mongo_uri)
db = client[database_name]
collection = db[collection_name]

csv_directory = "../server/static/data"

# Specify data types for each column in the CSV file
column_data_types = {
    "SCIENTIFIC NAME": str,
    "OBSERVATION COUNT": int,
    "LATITUDE": float,
    "LONGITUDE": float,
    "OBSERVATION DATE": lambda x: datetime.strptime(x, "%d.%m.%Y"),
    "STATE": str,
    "YEAR": int,
    "WEEK OF YEAR": int,
}

collection.delete_many({})

for filename in os.listdir(csv_directory):
    if filename.endswith(".csv"):
        file_path = os.path.join(csv_directory, filename)

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            # Use the first row as the header
            csv_reader = csv.DictReader(csvfile, delimiter=';')

            # Convert each row to a dictionary and insert into MongoDB
            for row in csv_reader:
                converted_row = {}
                for column, data_type in column_data_types.items():
                    converted_row[column] = data_type(row[column])

                # Insert converted row into MongoDB
                collection.insert_one(converted_row)

# Close MongoDB connection

collection_info_name = "species_information"
info_collection = db[collection_info_name]
info_collection.delete_many({})

# Information about species
species_information = [
    {"COMMON NAME": "Czapla biała",
     "SCIENTIFIC NAME": "Ardea alba",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Czapla_bia%C5%82a",
     "EBIRD LINK": "https://ebird.org/species/greegr/PL"
     },
    {"COMMON NAME": "Myszołów zwyczajny",
     "SCIENTIFIC NAME": "Buteo buteo",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Myszo%C5%82%C3%B3w_zwyczajny",
     "EBIRD LINK": "https://ebird.org/species/combuz1/PL"
     },
    {"COMMON NAME": "Biegus zmienny",
     "SCIENTIFIC NAME": "Calidris alpina",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Biegus_zmienny",
     "EBIRD LINK": "https://ebird.org/species/dunlin/PL"
     },
    {"COMMON NAME": "Batalion",
     "SCIENTIFIC NAME": "Calidris pugnax",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Batalion_(ptak)",
     "EBIRD LINK": "https://ebird.org/species/ruff/PL"
     },
    {"COMMON NAME": "Bocian biały",
     "SCIENTIFIC NAME": "Ciconia ciconia",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Bocian_bia%C5%82y",
     "EBIRD LINK": "https://ebird.org/species/whisto1/PL"
     },
    {"COMMON NAME": "Błotniak stawowy",
     "SCIENTIFIC NAME": "Circus aeruginosus",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/B%C5%82otniak_stawowy",
     "EBIRD LINK": "https://ebird.org/species/wemhar1/PL"
     },
    {"COMMON NAME": "Orlik grubodzioby",
     "SCIENTIFIC NAME": "Clanga clanga",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Orlik_grubodzioby",
     "EBIRD LINK": "https://ebird.org/species/grseag1/PL"
     },
    {"COMMON NAME": "Żuraw zwyczajny",
     "SCIENTIFIC NAME": "Grus grus",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/%C5%BBuraw_zwyczajny",
     "EBIRD LINK": "https://ebird.org/species/comcra/PL"
     },
    {"COMMON NAME": "Żołna zwyczajna",
     "SCIENTIFIC NAME": "Merops apiaster",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/%C5%BBo%C5%82na_zwyczajna",
     "EBIRD LINK": "https://ebird.org/species/eubeat1/PL"
     },
    {"COMMON NAME": "Pliszka siwa",
     "SCIENTIFIC NAME": "Motacilla alba",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Pliszka_siwa",
     "EBIRD LINK": "https://ebird.org/species/whiwag/PL"
     },
    {"COMMON NAME": "Pliszka cytrynowa",
     "SCIENTIFIC NAME": "Motacilla citreola",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Pliszka_cytrynowa",
     "EBIRD LINK": "https://ebird.org/species/citwag/PL"
     },
    {"COMMON NAME": "Orzechówka zwyczajna",
     "SCIENTIFIC NAME": "Nucifraga caryocatactes",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Orzech%C3%B3wka_zwyczajna",
     "EBIRD LINK": "https://ebird.org/species/eurnut1/PL"
     },
    {"COMMON NAME": "Kormoran zwyczajny",
     "SCIENTIFIC NAME": "Phalacrocorax carbo",
     "DESCRIPTION": "Sample description",
     "HABITAT": "Sample habitat",
     "WIKI LINK": "https://pl.wikipedia.org/wiki/Kormoran_zwyczajny",
     "EBIRD LINK": "https://ebird.org/species/grecor/PL"
     }
]

info_collection.insert_many(species_information)

client.close()
