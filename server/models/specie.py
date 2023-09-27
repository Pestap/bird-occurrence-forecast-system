from datetime import datetime

import pandas as pd
from abc import abstractmethod
from server.models.data_gathering.data_extraction_from_file import get_observations_state_groups
from server.models import enums


class Specie:

    def __init__(self):
        self.observation_data_grouped = None

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
        self.observation_data_grouped = {}
        observation_data_grouped_not_translated = get_observations_state_groups(self.get_csv_filepath())

        # Translate states and represent them as dictionary
        for state in observation_data_grouped_not_translated:
            self.observation_data_grouped[enums.translate_state_to_enum(state[0])] = state[1]

    def predict_autoregression(self, date_from, date_to):
        return None # In case no implementation

    def predict_neural_network(self, date_from, date_to):
        return None

    def make_predictions(self, model, date_from, date_to):
        self.load_observation_data_from_csv() # Loads observation data from csv into dictionary
        # TODO: maybe move to application startup

        predictions_dictionary = {}
        for state, observations in self.observation_data_grouped.items():

            # get last observation date

            last_observation_year = int(observations.tail(1)['YEAR'].to_numpy()[0])
            last_observation_month = int(observations.tail(1)['MONTH'].to_numpy()[0])

            last_observation_date = datetime(last_observation_year, last_observation_month, 1)

            # Get first observation date
            first_observation_year = int(observations.head(1)['YEAR'].to_numpy()[0])
            first_observation_month = int(observations.head(1)['MONTH'].to_numpy()[0])

            first_observation_date = datetime(first_observation_year, first_observation_month, 1)

            results = []
            months_between_last_and_from_date = (date_from.year - last_observation_date.year) * 12 +\
                                                (date_from.month - last_observation_date.month) # positive when from is after last
            months_between_last_and_to_date = (date_to.year - last_observation_date.year) * 12 + \
                                              (date_to.month - last_observation_date.month) # positive when to is after last

            if months_between_last_and_from_date < 0:
                if months_between_last_and_to_date < 0:
                    # get
                    observations_slice = observations[(observations['YEAR'] >= date_from.year) & (observations['YEAR'] <= date_to.year)].tail(-date_from.month + 1).head(date_to.month - 12)

                    observations_slice_values = observations_slice['OBSERVATION COUNT'].to_numpy()
                    observation_slice_months = observations_slice['MONTH'].to_numpy()
                    observation_slice_years = observations_slice['YEAR'].to_numpy()
                    observation_slice_dates = []

                    for i in range(len(observations_slice_values)):
                        observation_slice_dates.append(datetime(int(observation_slice_years[i]), int(observation_slice_months[i]), 1))

                    # Here: observations and corresponding dates can be returned
                    return observations_slice_values.tolist(), observation_slice_dates
                else:
                    pass # fetch some, predict months_between_last_and_to_date
            else:
                pass
                # normal prediction for mo
            # Check if from is before/inside/after



        if model == enums.Model.AUTOREGRESSION.name.lower():
            return self.predict_autoregression(date_from, date_to)
        elif model == enums.Model.NEURALNETWORK.name.lower():
            return self.predict_neural_network(date_from, date_to)

        return None