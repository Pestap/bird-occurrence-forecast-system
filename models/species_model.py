from abc import abstractmethod


class SpeciesModel:

    @abstractmethod
    def get_autoregression_models(self):
        pass