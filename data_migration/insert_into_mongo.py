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

# Information about species TODO: maybe change to wikipedia and eBird links
species_information = [
    {"COMMON NAME": "Great egret",
    "SCIENTIFIC NAME": "Ardea alba",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Common buzzard",
    "SCIENTIFIC NAME": "Buteo buteo",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Dunlin",
    "SCIENTIFIC NAME": "Calidris alpina",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Ruff",
    "SCIENTIFIC NAME": "Calidris pugnax",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "White Stork",
    "SCIENTIFIC NAME": "Ciconia ciconia",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Western marsh harrier",
    "SCIENTIFIC NAME": "Circus Aeruginosus",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Greater spotted eagle",
    "SCIENTIFIC NAME": "Clanga clanga",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Common crane",
    "SCIENTIFIC NAME": "Grus grus",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "European bee-eater",
    "SCIENTIFIC NAME": "Merops apiaster",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "White wagtail",
    "SCIENTIFIC NAME": "Motacilla alba",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Citrine wagtail",
    "SCIENTIFIC NAME": "Motacilla citreola",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Spotted nutcracker",
    "SCIENTIFIC NAME": "Nucifraga caryocatactes",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     },
    {"COMMON NAME": "Great cormorant",
    "SCIENTIFIC NAME": "Phalacrocorax carbo",
    "DESCRIPTION": "Sample description",
    "HABITAT": "Sample habitat",
     }
]

info_collection.insert_many(species_information)

client.close()
