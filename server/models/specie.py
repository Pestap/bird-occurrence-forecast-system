import pandas as pd
from abc import abstractmethod
from server.models.data_gathering.data_extraction_from_file import get_observations_state_groups
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

    @abstractmethod
    def get_csv_filepath(self):
        pass

    def load_observation_data_from_csv(self):
        self.observation_data_grouped = get_observations_state_groups(self.get_csv_filepath())
        for state in self.observation_data_grouped:
            state[0] = enums.translate_state_to_enum(state[0])

    def predict_autoregression(self, date_from, date_to):
        return None # In case no implementation

    def predict_neural_network(self, date_from, date_to):
        return None


    def predict(self, model, date_from, date_to):
        self.load_observation_data_from_csv()

        # Load observation data


        if model == enums.Model.AUTOREGRESSION.name.lower():
            return self.predict_autoregression(date_from, date_to)
        elif model == enums.Model.NEURALNETWORK.name.lower():
            return self.predict_neural_network(date_from, date_to)

        return None