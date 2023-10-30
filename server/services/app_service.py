from entities.species.ardea_alba import ArdeaAlba
from entities.species.ciconia_ciconia import CiconiaCiconia
from entities.species.circus_aeruginosus import CircusAeruginosus

# species dictionary
species = {
    'ardea_alba': ArdeaAlba(),
    'circus_aeruginosus': CircusAeruginosus(),
    'ciconia_ciconia': CiconiaCiconia(),

}


def get_species():
    return list(species.keys())


def get_specie_info(specie_name):
    try:
        return species[specie_name].get_info()
    except KeyError:
        return None


def get_specie_models(specie_name):
    try:
        return species[specie_name].get_available_models()
    except KeyError:
        return None


def predict_specie_with_model(specie_name, model, date_from, date_to, model_params, edge_date):
    try:
        predicted, test = species[specie_name].make_predictions(model, date_from, date_to, model_params, edge_date)
        prediction_error = calculate_mae_prediction(predicted, test)
        #return species[specie_name].make_predictions(model, date_from, date_to, model_params, edge_date)
        return predicted, test, prediction_error
    except KeyError:
        return None



def calculate_mae_prediction(predicted, test):
    predictions_to_test = {}
    for date, data in predicted.items():
        # if date is not in test
        if test.get(date) is None:
            continue
        predictions_to_test[date] = data

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

    errors_by_state = {}

    for state, data in observations_by_state.items():
        state_errors = []
        for date in data.keys():
            state_errors.append(abs((observations_by_state[state][date] - predictions_by_state[state][date])))

        errors_by_state[state] = sum(state_errors)/len(state_errors)

    return errors_by_state












