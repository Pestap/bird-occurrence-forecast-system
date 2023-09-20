from abc import abstractmethod


class Specie:

    @abstractmethod
    def get_autoregression_models(self):
        pass
    # TODO: add get moving average models - after research
    # TODO: add get DNN models - after research

    @abstractmethod
    def get_info(self):
        pass

    @abstractmethod
    def get_available_models(self):
        pass
