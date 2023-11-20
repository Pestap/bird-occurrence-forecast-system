import pandas as pd
from pymongo import MongoClient


class MongoDBRepository():
    def __init__(self, username="bird_app", password="Czapla#123", host="localhost", port=27017):
        self.username = username
        self.password = password
        self.host = host
        self.port = port

        self.database_name = "bird_occurrence_forecast_system"
        self.observation_collection_name = "observation_data"
        self.info_collection_name = "species_information"
        self.client = MongoClient(f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.database_name}")

        self.database = self.client[self.database_name]
        self.observation_collection = self.database[self.observation_collection_name]
        self.information_collection = self.database[self.info_collection_name]

    def get_observations_for_species(self, species_scientific_name):
        results = self.observation_collection.find({"SCIENTIFIC NAME": species_scientific_name})
        return pd.DataFrame(results)

    def get_information_for_species(self, species_scientific_name):
        results = self.information_collection.find_one({"SCIENTIFIC NAME": species_scientific_name})
        return results


repository = MongoDBRepository()