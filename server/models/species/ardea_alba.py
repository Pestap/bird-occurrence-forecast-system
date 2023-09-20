from server.models.autoregression.autoregression_model import AutoregressionModel
from server.models.specie import Specie
from server.models.states import State


class ArdeaAlba(Specie):
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