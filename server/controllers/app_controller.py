from datetime import datetime

from flask import Flask, request, jsonify, Response

import constants
from app import cache


from entities.enums import translate_enum_to_state
from services import app_service

from constants import LAST_OBSERVATION_DATE_STRING
# TODO: make all responses JSON (3/5)
def get_species():
    """
    Handle fetching all species
    """
    response = app_service.get_species()
    response_prepared = {"species": response}
    return jsonify(response_prepared)


def get_specie_info(specie_name):
    """
    Handle fetching specified specie information
    """
    response = app_service.get_specie_info(specie_name)

    if response is not None:
        return jsonify(response)

    return Response("Invalid specie name", status=400)


def get_specie_available_models(specie_name):
    """
    Handle fetching available models
    """

    response = app_service.get_specie_models(specie_name)

    response_prepared = {"supported_models": response}

    if response is not None:
        return jsonify(response_prepared) # throws 500 for now

    return Response("Invalid specie name", status=400)


def get_specie_model_information(specie_name, model):
    """
    Handle fetching specified model information for specie
    """
    return specie_name + "_" + model


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def get_observations(specie_name):
    try:
        date_from = datetime.strptime(request.args.get("from"), '%Y-%m-%d')
        date_to = datetime.strptime(request.args.get("to"), '%Y-%m-%d')
    except ValueError:
        return Response("Invalid date format", status=400)

    response = app_service.get_observations(specie_name, date_from, date_to)

    response_prepared = {"observations": response}

    if response is not None:
        return jsonify(response_prepared)  # throws 500 for now

    return Response("Invalid specie name", status=400)


@cache.cached(timeout=constants.CACHE_TIMEOUT, query_string=True)
def predict_specie_with_model(specie_name, model):

    try:
        date_from_datetime = datetime.strptime(request.args.get("from"), '%Y-%m-%d')
        date_to_datetime = datetime.strptime(request.args.get("to"), '%Y-%m-%d')


        # Replace months with 1
        date_to_datetime = date_to_datetime.replace(day=1)
        date_from_datetime = date_from_datetime.replace(day=1)
        # Check if dates are correct
        if date_from_datetime > date_to_datetime:
            return Response("Invalid data range, (from after to)", status=400)

        # Get edge date (for now no validation)


        edge_date_from_query = request.args.get("edge")

        if edge_date_from_query is None:
            edge_date_from_query = LAST_OBSERVATION_DATE_STRING

        try:
            edge_date = datetime.strptime(edge_date_from_query, '%Y-%m-%d')
        except ValueError:
            edge_date = datetime.strptime(LAST_OBSERVATION_DATE_STRING, '%Y-%m-%d')

        if edge_date > datetime.strptime(LAST_OBSERVATION_DATE_STRING, '%Y-%m-%d'):
            return Response("Parameter (edge) cannot exceed 2023-1-1 and cannot be before date_from", status=400)


        # Get model params from body and validate them
        model_params = {}

        model_params['autoregression_order'] = request.args.get("autoregression_order")

        validate_model_params(model_params)


        response = app_service.predict_specie_with_model(specie_name, model, date_from_datetime, date_to_datetime, model_params, edge_date)
        if response is not None:
            predictions = response[0]
            tests = response[1]
            prediction_errors = response[2]

            # Translate dates
            #{state: round(observation_value, 2)
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

            for state, data in prediction_errors.items():
                prediction_errors[state] = round(data, 2)

            # TODO: refactor
            predictions_v2 = {date: {} for date in predictions_translated.keys()}

            for date, empty_dict in predictions_v2.items():
                for state, value in predictions_translated[date].items():
                    empty_dict[translate_enum_to_state(state)] = value

            tests_v2 = {date: {} for date in tests_translated.keys()}

            for date, empty_dict in tests_v2.items():
                for state, value in tests_translated[date].items():
                    empty_dict[translate_enum_to_state(state)] = value

            prediction_errors_v2 = {translate_enum_to_state(state): value for state, value in prediction_errors.items()}


            response_object = {
                "predictions" : predictions_v2,
                "tests": tests_v2,
                "mae_errors": prediction_errors_v2

            }
            return jsonify(response_object)

        return Response("Invalid specie name", status=400)
    except ValueError:
        return Response("Invalid date format, try using YYYY-MM-DD", status=400)

    # 2012-09-01

def validate_model_params(model_params):
    params_to_check = ['autoregression_order']

    for param in model_params:
        if param in params_to_check and param in model_params:
            try:
                model_params[param] = int(model_params[param])
            except (ValueError, TypeError) as e:
                model_params[param] = None
