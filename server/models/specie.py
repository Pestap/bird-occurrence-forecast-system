from datetime import datetime
from statsmodels.tsa.ar_model import AutoReg
from abc import abstractmethod

from dateutil import rrule, relativedelta

from server.models.data_gathering.data_extraction_from_file import get_observations_state_groups
from server.models import enums


class Specie:

    def __init__(self):
        self.observation_data_grouped = None

    def get_autoregression_models(self):
        return None
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
        steps = self.get_autoregression_models()[state]

        if steps is None: # id steps is None it means that the specie does not support autoregression
            return None

        model = AutoReg(self.observation_data_grouped[state]['OBSERVATION COUNT'], lags=steps).fit()
        result = list(model.forecast(steps=months))
        result_non_negative = [val if val >=0 else 0 for val in result]

        return result_non_negative

    def predict_neural_network(self, date_from, date_to):
        return None

    def make_predictions_with_model(self, model, state, steps):
        if model.upper() == enums.Model.AUTOREGRESSION.name:
            return self.predict_autoregression(state, steps)
        else:
            return None

    def make_predictions(self, model, date_from, date_to):
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

        """
        
        READ OBSERVATIONS FROM DATA
        
        """

        if date_from <= datetime(2023, 1, 1): # read observations when desired by user
            observation_date_list = []

            # Create list of desired dates to read observations from:
            #TODO: maybe add constant for threshold date
            until_date = date_to if date_to < datetime(2023, 1, 1) else datetime(2023, 1, 1) # get the date to which read observations

            for dt in rrule.rrule(rrule.MONTHLY, dtstart=date_from, until=until_date): # until is hardcoded for now
                observation_date_list.append(dt)

            # Read observations
            for date in observation_date_list:
                predictions_dictionary[date] = {} # empty dictionary placeholder

                # iterate through observations by state
                for state, observations in self.observation_data_grouped.items():
                    # Query observations for desired date
                    try:
                        # read OBSERVATION COUNT and convert to float
                        value = float(observations.loc[(observations['YEAR'] == date.year) & (observations['MONTH'] == date.month)]['OBSERVATION COUNT'].to_numpy()[0])
                        predictions_dictionary[date][state.name] = value
                    except IndexError: # Exception is thrown by accessing [0] index in empty array - no observation found
                        predictions_dictionary[date][state.name] = None # if no observation found for specified date - None => null

        """
        
        MAKE PREDICTIONS
        
        """

        # Calculate how many months to predict
        delta = relativedelta.relativedelta(date_to, datetime(2023, 1, 1))
        months_from_last_observation_data = delta.months + (delta.years * 12)

        if months_from_last_observation_data > 0: # predict only if needed
            prediction_date_list = []

            # TODO: maybe add constant for dtstart
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=datetime(2023, 2, 1), until=date_to): # start date hardcoded - 2023.02.01 - first month for which we do not have observations
                prediction_date_list.append(dt)

            # iterate through states and make predictions
            for state in self.observation_data_grouped.keys():
                # make predictions with model: implementation by desired specie
                predictions = self.make_predictions_with_model(model, state, months_from_last_observation_data)
                # If incorrect model selected
                if predictions is None:
                    return None

                # add results to prediction_dictionary
                predictions_with_dates = {prediction_date_list[i]: predictions[i] for i in range(len(predictions))}
                for date in prediction_date_list:
                    # append predictions to predictions_dictionary
                    if predictions_dictionary.get(date) is None: # if there is no entry for specific date, add one (empty dictionary)
                        predictions_dictionary[date] = {}

                    predictions_dictionary[date][state.name] = predictions_with_dates[date] # add prediction to appropriate dictionary

        if date_from > datetime(2023, 1, 1): # if date from is after last observation data, remove entries after 2023.01.01 and before date_to
            predictions_dictionary = {date: value for date, value in predictions_dictionary.items() if date >= date_from}

        return predictions_dictionary
