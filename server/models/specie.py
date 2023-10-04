from datetime import datetime

import pandas as pd
from abc import abstractmethod

from dateutil import rrule, relativedelta

from server.models.data_gathering.data_extraction_from_file import get_observations_state_groups
from server.models import enums


class Specie:

    def __init__(self):
        self.observation_data_grouped = None


    @abstractmethod
    def get_autoregression_models(self):
        pass
    # TODO: include first observation date (maybe also last?) in get_info
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

    def predict_autoregression(self, state, months):
        return None # In case no implementation

    def predict_neural_network(self, date_from, date_to):
        return None

    def make_predictions(self, model, date_from, date_to):
        month_from = date_from.month
        year_from = date_from.year

        month_to = date_to.month
        year_to = date_to.year

        predictions_dictionary = {}
        """
        predictions_dictionary structure:
        {
            year-month1:{
                state1: value
                state2: value
                ...
            },
            year-month2: {
                state1: value
                state2: value    
            }
        }
        """

        # For now I assume that all states have observations till 1-2023
        # Earliest records are from 1990-1

        if date_from <= datetime(2023, 1, 1):
            desired_date_list = []

            # Create list of desired dates to read observations from:
            until_date = date_to if date_to < datetime(2023, 1, 1) else datetime(2023, 1, 1)
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=date_from, until=until_date): # until is hardcoded for now
                desired_date_list.append(dt)
            # Read observations
            for date in desired_date_list:
                predictions_dictionary_key = f"{date.year}-{date.month}"
                predictions_dictionary[predictions_dictionary_key] = {} # empty dictionary

                for state, observations in self.observation_data_grouped.items():
                    # Query observations for desired date
                    try:
                        value = float(observations.loc[(observations['YEAR'] == date.year) & (observations['MONTH'] == date.month)]['OBSERVATION COUNT'].to_numpy()[0])
                        predictions_dictionary[predictions_dictionary_key][state.name] = value
                    except IndexError: # Exception is thrown by accessing [0] index in empty array - no observation found
                        predictions_dictionary[predictions_dictionary_key][state.name] = None

        # Make predictions

        # Calculate how many months to predict

        delta = relativedelta.relativedelta(date_to, datetime(2023,1,1))
        months_from_last_observation_data = delta.months + (delta.years * 12)


        if months_from_last_observation_data > 0:
            # TODO: rename to prediction date list, the other one to observation date list
            desired_date_list = []

            for dt in rrule.rrule(rrule.MONTHLY, dtstart=datetime(2023, 2, 1), until=date_to): # until is hardcoded for now
                desired_date_list.append(dt)

            for state in self.observation_data_grouped.keys():
                # TODO: predictions by different methods (if else)
                predictions = self.predict_autoregression(state, months_from_last_observation_data)
                # predict for every state for months_from_last_observation_data
                # add results to prediction_dictionary
                predictions_with_dates = {desired_date_list[i]: predictions[i] for i in range(len(predictions))}
                for date in desired_date_list:
                    # append predictions to predictions_dictionary
                    predictions_dictionary_key = f"{date.year}-{date.month}"
                    if predictions_dictionary.get(predictions_dictionary_key) is None:
                        predictions_dictionary[predictions_dictionary_key] = {}

                    predictions_dictionary[predictions_dictionary_key][state.name] = predictions_with_dates[date]

        if date_from > datetime(2023, 1, 1):
            pass
            # Delete dictionary entries before that date




        return predictions_dictionary



        if model == enums.Model.AUTOREGRESSION.name.lower():
            return self.predict_autoregression(date_from, date_to)
        elif model == enums.Model.NEURALNETWORK.name.lower():
            return self.predict_neural_network(date_from, date_to)
        return None