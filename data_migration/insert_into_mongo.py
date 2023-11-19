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
client.close()
