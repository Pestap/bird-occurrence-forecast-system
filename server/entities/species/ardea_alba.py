from entities.specie import Specie
from entities.enums import State, Model



class ArdeaAlba(Specie):

    def __init__(self):
        self.common_name = "Great egret"
        self.scientific_name = "Ardea alba"
        self.desription = "Ardea Alba sample description"
        self.habitat = "Ardea Alba sample habititat"
        self.observation_csv_path = "static/data/ardea_alba.csv" # path is relative from app.py
        self.load_observation_data_from_csv()


    def get_csv_filepath(self):
        return self.observation_csv_path

    def get_info(self):
        return {"scientific_name": self.scientific_name,
                "common_name": self.common_name,
                "description": self.description,
                "habitat": self.habitat}

    def get_available_models(self):
        return [Model.AUTOREGRESSION.name.lower(),
                Model.ARMA.name.lower()]

    def get_autoregression_models(self):
        return {State.DOLNOSLASKIE: 34,
                State.KUJAWSKO_POMORSKIE: 25,
                State.LUBELSKIE: 36,
                State.LUBUSKIE: 24,
                State.LODZKIE: 26,
                State.MALOPOLSKIE: 29,
                State.MAZOWIECKIE: 22,
                State.OPOLSKIE: 36,
                State.PODKARPACKIE: 24,
                State.PODLASKIE: 32,
                State.POMORSKIE: 26,
                State.SLASKIE: 35,
                State.SWIETOKRZYSKIE: 36,
                State.WARMINSKO_MAZURSKIE: 24,
                State.WIELKOPOLSKIE: 34,
                State.ZACHODNIOPOMORSKIE: 35,
                }

