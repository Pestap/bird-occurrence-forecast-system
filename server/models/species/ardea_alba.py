import pandas as pd

from server.models.autoregression.autoregression_model import AutoregressionModel
from server.models.specie import Specie
from server.models.enums import State, Model

class ArdeaAlba(Specie):

    def __init__(self): # FIXME: change to relative path
        self.observation_csv_path = "D:\\Piotrek\\inzynierka\\bird-occurence-forecast-system\\data\\ardea_alba.csv"

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




    def get_autoregression_models(self) -> list[AutoregressionModel]:
        return [
            AutoregressionModel(State.DOLNOSLASKIE, 34),
            AutoregressionModel(State.KUJAWSKO_POMORSKIE, 25),
            AutoregressionModel(State.LUBELSKIE, 36),
            AutoregressionModel(State.LUBUSKIE, 24),
            AutoregressionModel(State.LODZKIE, 26),
            AutoregressionModel(State.MALOPOLSKIE, 29),
            AutoregressionModel(State.MAZOWIECKIE, 22),
            AutoregressionModel(State.OPOLSKIE, 36),
            AutoregressionModel(State.PODKARPACKIE, 24),
            AutoregressionModel(State.PODLASKIE, 32),
            AutoregressionModel(State.POMORSKIE, 26),
            AutoregressionModel(State.SLASKIE, 35),
            AutoregressionModel(State.SWIETOKRZYSKIE, 36),
            AutoregressionModel(State.WARMINSKO_MAZURSKIE, 24),
            AutoregressionModel(State.WIELKOPOLSKIE, 34),
            AutoregressionModel(State.ZACHODNIOPOMORSKIE, 35)
        ]