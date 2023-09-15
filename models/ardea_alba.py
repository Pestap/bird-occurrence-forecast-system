from models.autoregression.autoregression_model import AutoregressionModel
from models.species_model import SpeciesModel
from models.states import State


class ArdeaAlbaModel(SpeciesModel):

    @staticmethod
    def get_autoregression_models() -> list[AutoregressionModel]:
        return [
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
            AutoregressionModel(State.ZACHODNIOPOMORSKIE, 0),
        ]