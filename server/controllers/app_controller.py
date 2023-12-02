from datetime import datetime
from flask import request, jsonify, Response
import constants
from cache.cache_module import cache
from entities.enums import translate_enum_to_state
from services import app_service
from entities.prediction_models.models import get_model_params
from constants import LAST_OBSERVATION_DATE_STRING, EDGE_DATE_DEFAULT


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def get_species():
    """
    Handle fetching all species
    """
    response = app_service.get_species()

    # create response in JSON format
    response_prepared = {"species": response}
    return jsonify(response_prepared)


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def get_species_info(species_name):
    """
    Handle fetching specified species information
    """
    response = app_service.get_species_info(species_name)

    if response is not None:
        return jsonify(response)

    return Response("Invalid species name", status=400)


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def get_species_available_models(species_name):
    """
    Handle fetching available models
    """

    response = app_service.get_species_models(species_name)

    response_prepared = {"supported_models": response}

    if response is not None:
        return jsonify(response_prepared)

    return Response("Invalid species name", status=400)


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def get_species_model_information(species_name, model):
    """
    Handle fetching specified model information for species

    """
    available_models = app_service.get_species_models(species_name)

    if available_models is None:
        return Response("Invalid species name", status=404)

    if model in [m['value'] for m in available_models]:
        result = get_model_params(model)
        if result is not None:
            return jsonify(result)

    return Response("Selected species does not support selected model", status=404)


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def get_observations(species_name):
    """
    Handle fetching observations
    """
    try: # Try to parse dates
        date_from = datetime.strptime(request.args.get("from"), '%Y-%m-%d')
        date_to = datetime.strptime(request.args.get("to"), '%Y-%m-%d')
    except ValueError:
        return Response("Invalid date format", status=400)

    response = app_service.get_observations(species_name, date_from, date_to)
    response_prepared = {"observations": response}

    if response is not None:
        return jsonify(response_prepared)

    return Response("Invalid species name", status=400)


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def predict_species_with_model(species_name, model):
    """
    Handle predictions
    """
    try:
        date_from_datetime = datetime.strptime(request.args.get("from"), '%Y-%m')
        date_to_datetime = datetime.strptime(request.args.get("to"), '%Y-%m')

        # Check if dates are correct
        if date_from_datetime > date_to_datetime:
            return Response("Invalid data range, (from after to)", status=400)

    except ValueError:
        return Response("Invalid date format: should be %Y-%m", status=400)
    except TypeError:
        return Response("Missing query parameters: from, to", status=400)

    # get edge date
    edge_date_from_query = request.args.get("edge")

    if edge_date_from_query is None: # if none set to default
        edge_date_from_query = EDGE_DATE_DEFAULT

    # try to parse
    edge_date = datetime.strptime(edge_date_from_query, '%Y-%m')

    # check if edge date is valid
    if edge_date > datetime.strptime(LAST_OBSERVATION_DATE_STRING, '%Y-%m-%d'):
        return Response("Parameter (edge) cannot exceed 2023-1-1 and cannot be before date_from", status=400)

    # Get model params from body and validate them
    model_params = {'autoregression_order': request.args.get("autoregression_order"),
                    'moving_average_order': request.args.get("moving_average_order"),
                    'differencing_order': request.args.get("differencing_order")}

    validate_model_params(model_params)

    response = app_service.predict_species_with_model(species_name, model, date_from_datetime, date_to_datetime, model_params, edge_date)

    if response is None:
        return Response("Something went wrong while caluculating predictions,"
                        " make sure the model parameters are correct", status=400)

    predictions = response[0]
    tests = response[1]
    mae_errors = response[2]
    mape_errors = response[3]
    rmse_errors = response[4]
    custom_errors = response[5]

    # Translate dates
    predictions_translated = {f"{date.year}-{date.month:0>{2}}": value for date, value in predictions.items()}
    tests_translated = {f"{date.year}-{date.month:0>{2}}": value for date, value in tests.items()}

    # Round numbers and translate states to string
    for date, data in predictions_translated.items():
        for state, observation_value in data.items():

            if observation_value is not None:
                predictions_translated[date][state] = round(observation_value, 2)

    for date, data in tests_translated.items():
        for state, observation_value in data.items():

            if observation_value is not None:
                tests_translated[date][state] = round(observation_value, 2)

    for state, data in mae_errors.items():
        if data is not None:
            mae_errors[state] = round(data, 2)

    for state, data in mape_errors.items():
        if data is not None:
            mape_errors[state] = round(data, 2)

    for state, data in rmse_errors.items():
        if data is not None:
            rmse_errors[state] = round(data, 2)

    for state, data in custom_errors.items():
        if data is not None:
            custom_errors[state] = round(data, 2)

    predictions_v2 = {date: {} for date in predictions_translated.keys()}

    for date, empty_dict in predictions_v2.items():
        for state, value in predictions_translated[date].items():
            if value is not None:
                empty_dict[translate_enum_to_state(state)] = value

    tests_v2 = {date: {} for date in tests_translated.keys()}

    for date, empty_dict in tests_v2.items():
        for state, value in tests_translated[date].items():
            if value is not None:
                empty_dict[translate_enum_to_state(state)] = value

    mae_errors_v2 = {translate_enum_to_state(state): value for state, value in mae_errors.items()}
    mape_errors_v2 = {translate_enum_to_state(state): value for state, value in mape_errors.items()}
    rmse_errors_v2 = {translate_enum_to_state(state): value for state, value in rmse_errors.items()}
    custom_errors_v2 = {translate_enum_to_state(state): value for state, value in custom_errors.items()}

    response_object = {
        "predictions" : predictions_v2,
        "tests": tests_v2,
        "mae_errors": mae_errors_v2,
        "mape_errors": mape_errors_v2,
        "rmse_errors": rmse_errors_v2,
        "custom_errors": custom_errors_v2
    }

    return jsonify(response_object)


def validate_model_params(model_params):
    params_to_check = ['autoregression_order', 'moving_average_order', 'differencing_order']

    for param in model_params:
        if param in params_to_check and param in model_params:
            try:
                model_params[param] = int(model_params[param])
            except (ValueError, TypeError) as e:
                model_params[param] = None
