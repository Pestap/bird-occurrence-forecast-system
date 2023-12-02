from entities.species_base import Species
from entities.enums import State, Model


class CiconiaCiconia(Species):

    def __init__(self):
        super().__init__()
        self.common_name = "White Strok"
        self.scientific_name = "Ciconia ciconia"
        self.description = "White stork sample description"
        self.habitat = "White stork sample habititat"
        self.observation_csv_path = "static/data/ciconia_ciconia.csv"  # path is relative from app.py
        self.load_observation_data()
        self.load_species_info()

    def get_csv_filepath(self):
        return self.observation_csv_path

    def get_available_models_for_species(self):
        return []

    def get_autoregression_models(self):
        return {State.DOLNOSLASKIE: 36,
                State.KUJAWSKO_POMORSKIE: 36,
                State.LUBELSKIE: 36,
                State.LUBUSKIE: 35,
                State.LODZKIE: 24,
                State.MALOPOLSKIE: 36,
                State.MAZOWIECKIE: 25,
                State.OPOLSKIE: 33,
                State.PODKARPACKIE: 24,
                State.PODLASKIE: 36,
                State.POMORSKIE: 32,
                State.SLASKIE: 36,
                State.SWIETOKRZYSKIE: 35,
                State.WARMINSKO_MAZURSKIE: 36,
                State.WIELKOPOLSKIE: 36,
                State.ZACHODNIOPOMORSKIE: 36,
                }
