from datetime import datetime

from flask import Flask, request, jsonify, Response

from server.models.enums import translate_enum_to_state
from server.services import app_service


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

        # Get model params from body and validate them
        model_params = {}

        model_params['autoregression_order'] = request.args.get("autoregression_order")

        validate_model_params(model_params)





        response = app_service.predict_specie_with_model(specie_name, model, date_from_datetime, date_to_datetime, model_params)
        if response is not None:
            # Translate dates
            #{state: round(observation_value, 2)
            response_translated = {f"{date.year}-{date.month:0>{2}}": value for date, value in response.items()}

            # Round numbers and translate states to string
            for date, data in response_translated.items():
                for state, observation_value in data.items():

                    if observation_value is not None:
                        response_translated[date][state] = round(observation_value, 2)

            # TODO: refactor
            response_v2 = {date: {} for date in response_translated.keys()}

            for date, empty_dict in response_v2.items():
                for state, value in response_translated[date].items():
                    empty_dict[translate_enum_to_state(state)] = value


            return jsonify(response_v2)

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
