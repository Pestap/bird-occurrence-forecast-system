from typing import Dict, Union, Any

import pandas as pd

from server.models.autoregression.autoregression_model import AutoregressionModel
from server.models.specie import Specie
from server.models.enums import State, Model

class ArdeaAlba(Specie):

    def __init__(self): # FIXME: change to relative path
        self.observation_csv_path = "D:\\Piotrek\\inzynierka\\bird-occurence-forecast-system\\data\\ardea_alba.csv"
        self.load_observation_data_from_csv()

    def get_csv_filepath(self):
        return self.observation_csv_path

    def get_info(self):
        description = "Ardea Alba sample description"
        habitat = "Ardea Alba sample habititat"

        dict = {"description": description,
                "habitat": habitat}
        return dict

    def get_available_models(self):
        return [Model.AUTOREGRESSION.name]

    def predict_autoregression(self, date_from, date_to):
        return 10

    def get_autoregression_models(self) -> dict[int, int]:
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

