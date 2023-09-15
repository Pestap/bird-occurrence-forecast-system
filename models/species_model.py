from abc import abstractmethod


class SpeciesModel:

    @abstractmethod
    def get_autoregression_models(self):
        pass
    # TODO: add get moving average models - after research
    # TODO: add get DNN models - after research