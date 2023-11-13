from entities.species_base import Specie
from entities.enums import State, Model


class GrusGrus(Specie):

    def __init__(self):
        self.common_name = "Common crane"
        self.scientific_name = "Grus Grus"
        self.description = "Grus Grus sample description"
        self.habitat = "Grus Grus sample habititat"
        self.observation_csv_path = "static/data/grus_grus.csv" # path is relative from app.py
        self.load_observation_data_from_csv()


    def get_csv_filepath(self):
        return self.observation_csv_path

    def get_available_models_for_species(self):
        return []

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

