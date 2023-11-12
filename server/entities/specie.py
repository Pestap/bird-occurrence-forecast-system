from datetime import datetime
from statsmodels.tsa.ar_model import AutoReg
from abc import abstractmethod

from dateutil import rrule, relativedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX

from entities.data_gathering.data_extraction_from_file import get_observations
from entities import enums

from constants import LAST_OBSERVATION_DATE_STRING


class Specie:

    def __init__(self):
        self.observation_data_grouped = None
        self.observations_df = None

    def get_autoregression_models(self):
        return None
    # TODO: include first observation date (maybe also last?) in get_info
    # TODO: add get moving average models - after research
    # TODO: add get DNN models - after research

    def get_info(self):
        return {"scientific_name": self.scientific_name,
                "common_name": self.common_name,
                "description": self.description,
                "habitat": self.habitat}


    def get_available_models(self):
        result = self.get_available_models_for_species()
        result += [enums.Model.AUTOREGRESSION.name.lower(),
                   enums.Model.ARMA.name.lower()] # append models applicable to all species
        return result

    @abstractmethod
    def get_available_models_for_species(self):
        pass

    @abstractmethod
    def get_csv_filepath(self):
        pass

    def load_observation_data_from_csv(self):
        self.observation_data_grouped = {}
        observation_data_grouped_not_translated, observations = get_observations(self.get_csv_filepath())

        # Translate states and represent them as dictionary
        for state in observation_data_grouped_not_translated:
            self.observation_data_grouped[enums.translate_state_to_enum(state[0])] = state[1]

        self.observations_df = observations
        print(f"SPECIES LOADED: {self.scientific_name}")

    def get_observations(self, date_from, date_to):
        df = self.observations_df
        filtered_observations = df.loc[(df['OBSERVATION DATE'] >= date_from) & (df['OBSERVATION DATE'] <= date_to)]
        filtered_observations.sort_values(by='OBSERVATION DATE', ascending=True, inplace=True)
        dictionaries_list = filtered_observations.to_dict('records')

        # change keys
        for obsevation_fact in dictionaries_list:
            obsevation_fact['observation count'] = obsevation_fact['OBSERVATION COUNT']
            del obsevation_fact['OBSERVATION COUNT']
            obsevation_fact['observation date'] = obsevation_fact['OBSERVATION DATE']
            del obsevation_fact['OBSERVATION DATE']
            obsevation_fact['latitude'] = obsevation_fact['LATITUDE']
            del obsevation_fact['LATITUDE']
            obsevation_fact['longitude'] = obsevation_fact['LONGITUDE']
            del obsevation_fact['LONGITUDE']

        return dictionaries_list

    def predict_autoregression(self, state, months, user_ar_order=None):
        steps = user_ar_order

        if steps is None:
            steps = self.get_autoregression_models()[state]

        # if steps is None it means that the specie does not support autoregression
        if steps is None:
            return None

        model = AutoReg(self.observation_data_grouped[state]['OBSERVATION COUNT'], lags=steps, seasonal=True, period=12).fit()
        result = list(model.forecast(steps=months))
        result_non_negative = [val if val >= 0 else 0 for val in result]

        return result_non_negative

    def predict_arma(self, state, months):
        #steps = self.get_autoregression_models()[state]
        ar_steps = 12
        ma_steps = 6
        i_steps = 2
        if ar_steps is None or ma_steps is None:
            return None

        model = SARIMAX(self.observation_data_grouped[state]['OBSERVATION COUNT'], order=(ar_steps, i_steps, ma_steps), alpha=0.95)
        results = model.fit()
        #results = list(model.predict(start=len(self.observation_data_grouped[state]['OBSERVATION COUNT']), end=len(self.observation_data_grouped[state]['OBSERVATION COUNT'])) + months)

        predictions = list(results.forecast(steps=months))
        predictions_non_negative = [val if val >= 0 else 0 for val in predictions]

        return predictions_non_negative


    def predict_sarima(self, state, months):
        pass
    def predict_neural_network(self, date_from, date_to):
        return None

    def make_predictions_with_model(self, model, model_params, state, steps):
        if model.upper() == enums.Model.AUTOREGRESSION.name:

            return self.predict_autoregression(state, steps, model_params['autoregression_order'] if 'autoregression_order' in model_params else None)
        elif model.upper() == enums.Model.ARMA.name:
            return self.predict_arma(state, steps)
        else:
            return None

    def make_predictions(self, model, date_from, date_to, model_params, edge_date):
        predictions_dictionary = {}
        test_observation_dictionary = {}


        # For now I assume that all states have observations till 1-2023
        # Earliest records are from 1990-1

        #edge_date = datetime(2023,1,1)

        """
        
        READ OBSERVATIONS FROM DATA
        
        """


        if date_from <= datetime.strptime(LAST_OBSERVATION_DATE_STRING, '%Y-%m-%d'): # read observations when desired by user
            observation_date_list = []
            observations_dictionary = {}

            # Create list of desired dates to read observations from:
            #TODO: maybe add constant for threshold date
            until_date = date_to if date_to < datetime.strptime(LAST_OBSERVATION_DATE_STRING, '%Y-%m-%d') else datetime.strptime(LAST_OBSERVATION_DATE_STRING, '%Y-%m-%d') # get the date to which read observations

            for dt in rrule.rrule(rrule.MONTHLY, dtstart=date_from, until=until_date): # until is hardcoded for now
                observation_date_list.append(dt)

            # Read observations
            for date in observation_date_list:
                observations_dictionary[date] = {} # empty dictionary placeholder

                # iterate through observations by state
                for state, observations in self.observation_data_grouped.items():
                    # Query observations for desired date
                    try:
                        # read OBSERVATION COUNT and convert to float
                        value = float(observations.loc[(observations['YEAR'] == date.year) & (observations['MONTH'] == date.month)]['OBSERVATION COUNT'].to_numpy()[0])
                        observations_dictionary[date][state.name] = value
                    except IndexError: # Exception is thrown by accessing [0] index in empty array - no observation found
                        observations_dictionary[date][state.name] = None # if no observation found for specified date - None => null

            # Split the data into training and test?

            for date, data in observations_dictionary.items():
                if date <= edge_date:
                    predictions_dictionary[date] = data
                else:
                    test_observation_dictionary[date] = data


        """
        
        MAKE PREDICTIONS
        
        """

        # Calculate how many months to predict
        delta = relativedelta.relativedelta(date_to, edge_date)
        months_from_last_observation_data = delta.months + (delta.years * 12)

        if months_from_last_observation_data > 0: # predict only if needed
            prediction_date_list = []

            # TODO: maybe add constant for dtstart
            for dt in rrule.rrule(rrule.MONTHLY, dtstart=edge_date, until=date_to): # start date hardcoded - 2023.02.01 - first month for which we do not have observations
                prediction_date_list.append(dt)

            prediction_date_list = prediction_date_list[1::]

            # iterate through states and make predictions
            for state in self.observation_data_grouped.keys():
                # make predictions with model: implementation by desired specie
                predictions = self.make_predictions_with_model(model, model_params, state, months_from_last_observation_data)
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


        # Cut unnecessary results
        if date_from > edge_date: # if date from is after last observation data, remove entries after 2023.01.01 and before date_to
            predictions_dictionary = {date: value for date, value in predictions_dictionary.items() if date >= date_from}

        return predictions_dictionary, test_observation_dictionary
