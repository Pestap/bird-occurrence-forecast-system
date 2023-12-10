import math

from entities.species.ardea_alba import ArdeaAlba
from entities.species.buteo_buteo import ButeoButeo
from entities.species.calidris_alpina import CalidrisAlpina
from entities.species.calidris_pugnax import CalidrisPugnax
from entities.species.ciconia_ciconia import CiconiaCiconia
from entities.species.circus_aeruginosus import CircusAeruginosus
from entities.species.clanga_clanga import ClangaClanga
from entities.species.grus_grus import GrusGrus
from entities.species.merops_apiaster import MeropsApiaster
from entities.species.motacilla_alba import MotacillaAlba
from entities.species.motacilla_citreola import MotacillaCitreola
from entities.species.nucifraga_caryocatactes import NucifragaCaryocatactes
from entities.species.phalacrocorax_carbo import PhalacrocoraxCarbo

from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error

# species dictionary
species = {
    'ardea_alba': ArdeaAlba(),
    'circus_aeruginosus': CircusAeruginosus(),
    'ciconia_ciconia': CiconiaCiconia(),
    'clanga_clanga': ClangaClanga(),
    'motacilla_alba': MotacillaAlba(),
    'motacilla_citreola': MotacillaCitreola(),
    'merops_apiaster': MeropsApiaster(),
    'buteo_buteo': ButeoButeo(),
    'nucifraga_caryocatactes': NucifragaCaryocatactes(),
    'grus_grus': GrusGrus(),
    'calidris_pugnax': CalidrisPugnax(),
    'calidris_alpina': CalidrisAlpina(),
    'phalacrocorax_carbo': PhalacrocoraxCarbo()

}


def get_species():
    return sorted(list(species.keys()))


def get_species_info(species_name):
    try:
        return species[species_name].get_info()
    except KeyError:
        return None


def get_species_models(species_name):
    try:
        return species[species_name].get_available_models()
    except KeyError:
        return None


def get_observations(species_name, date_from, date_to):
    try:
        return species[species_name].get_observations(date_from, date_to)
    except KeyError:
        return None


def predict_species_with_model(specie_name, model, date_from, date_to, model_params, edge_date):
    try: # add try catch  - in case of None from predictions
        predicted, test = species[specie_name].make_predictions(model, date_from, date_to, model_params, edge_date)
        mae_errors = calculate_prediction_error(predicted, test, calculate_mae)
        mape_errors = calculate_prediction_error(predicted, test, calculate_mape)
        rmse_errors = calculate_prediction_error(predicted, test, calculate_rmse)
        custom_errors = calculate_prediction_error(predicted, test, calculate_custom_error)
        return predicted, test, mae_errors, mape_errors, rmse_errors, custom_errors
    except (KeyError, TypeError) as ex:
        return None


def calculate_prediction_error(predicted, test, error_function):

    predictions_by_state = {}
    observations_by_state = {}

    for date in test.keys():
        for state, observation_count in test[date].items():
            if predictions_by_state.get(state) is None:
                predictions_by_state[state] = {}
            predictions_by_state[state][date] = observation_count

        for state, observation_count in predicted[date].items():
            if observations_by_state.get(state) is None:
                observations_by_state[state] = {}
            observations_by_state[state][date] = observation_count

    # calculate and return approperiate error
    return error_function(observations_by_state, predictions_by_state)


def calculate_mape(observations_by_state, predictions_by_state):
    errors_by_state = {}

    for state, data in observations_by_state.items():
        state_errors = []
        for date in data.keys():
            predicted = predictions_by_state[state][date]
            observed = observations_by_state[state][date]

            if observed == 0:
                continue # we do not take records with zero into account TODO: maybe put 1?
            else:
                state_errors.append(abs(observed-predicted)/observed)

        errors_by_state[state] = sum(state_errors) / len(state_errors) if len(state_errors) > 0 else None


    return errors_by_state


def calculate_mae(observations_by_state, predictions_by_state):
    errors_by_state = {}

    for state, data in observations_by_state.items():
        predicted = []
        observed = []

        for date in data.keys():
            predicted.append(predictions_by_state[state][date])
            observed.append(observations_by_state[state][date])

        errors_by_state[state] = mean_absolute_error(observed, predicted)

    return errors_by_state


def calculate_rmse(observations_by_state, predictions_by_state):
    errors_by_state = {}

    for state, data in observations_by_state.items():
        predicted = []
        observed = []
        for date in data.keys():
            predicted.append(predictions_by_state[state][date])
            observed.append(observations_by_state[state][date])

        errors_by_state[state] = math.sqrt(mean_squared_error(observed, predicted))

    return errors_by_state


def calculate_custom_error(observations_by_state, predictions_by_state):
    errors_by_state = {}

    for state, data in observations_by_state.items():
        state_errors = []
        for date in data.keys():
            predicted = predictions_by_state[state][date]
            observed = observations_by_state[state][date]

            if predicted > 0.2 and observed > 0.2:
                state_errors.append(0)
            elif predicted <= 0.2 and observed <= 0.2:
                state_errors.append(0)
            else:
                state_errors.append(1)


        errors_by_state[state] = sum(state_errors)/len(state_errors)

    return errors_by_state











