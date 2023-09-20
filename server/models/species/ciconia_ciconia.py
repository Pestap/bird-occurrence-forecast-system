from server.models.autoregression.autoregression_model import AutoregressionModel
from server.models.specie import Specie
from server.models.enums import State


class CiconiaCiconia(Specie):
    def get_info(self):
        description = "Ciconia ciconia desc"
        habitat = "Ciconia habitat"

        dict = {"description": description,
                "habitat": habitat}
        return dict

    def get_autoregression_models(self) -> list[AutoregressionModel]:
        return [

            # TODO: Test models for ciconia_ciconia.csv
            AutoregressionModel(State.DOLNOSLASKIE, 0),
            AutoregressionModel(State.KUJAWSKO_POMORSKIE, 0),
            AutoregressionModel(State.LUBELSKIE, 0),
            AutoregressionModel(State.LUBUSKIE, 0),
            AutoregressionModel(State.LODZKIE, 0),
            AutoregressionModel(State.LODZKIE, 0),
            AutoregressionModel(State.MALOPOLSKIE, 0),
            AutoregressionModel(State.MAZOWIECKIE, 0),
            AutoregressionModel(State.OPOLSKIE, 0),
            AutoregressionModel(State.PODKARPACKIE, 0),
            AutoregressionModel(State.PODLASKIE, 0),
            AutoregressionModel(State.POMORSKIE, 0),
            AutoregressionModel(State.SLASKIE, 0),
            AutoregressionModel(State.SWIETOKRZYSKIE, 0),
            AutoregressionModel(State.WIELKOPOLSKIE, 0),
            AutoregressionModel(State.ZACHODNIOPOMORSKIE, 0)
        ]