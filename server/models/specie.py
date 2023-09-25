from abc import abstractmethod

from server.models import enums


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

    def predict_autoregression(self, date_from, date_to):
        return None # In case no implementation

    def predict_neural_network(self, date_from, date_to):
        return None

    def predict(self, model, date_from, date_to):

        if model == enums.Model.AUTOREGRESSION.name.lower():
            return self.predict_autoregression(date_from, date_to)
        elif model == enums.Model.NEURALNETWORK.name.lower():
            return self.predict_neural_network(date_from, date_to)

        return None