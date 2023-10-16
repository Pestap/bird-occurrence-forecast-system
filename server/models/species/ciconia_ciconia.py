from server.models.autoregression.autoregression_model import AutoregressionModel
from server.models.specie import Specie
from server.models.enums import State, Model


class CiconiaCiconia(Specie):

    def __init__(self):
        self.observation_csv_path = "static/data/ciconia_ciconia.csv"  # path is relative from app.py
        self.load_observation_data_from_csv()

    def get_csv_filepath(self):
        return self.observation_csv_path

    def get_info(self):
        common_name = "White Strok"
        scientific_name = "Ciconia ciconia"
        description = "Ardea Alba sample description"
        habitat = "Ardea Alba sample habititat"

        dict = {"scientific_name": scientific_name,
                "common_name": common_name,
                "description": description,
                "habitat": habitat}
        return dict

    def get_available_models(self):
        return [Model.AUTOREGRESSION.name.lower()]

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
