from datetime import datetime

from flask import Flask, request, jsonify, Response

from server.services import app_service


# TODO: make all responses JSON (3/5)
def get_species():
    """
    Handle fetching all species
    """
    return jsonify(app_service.get_species())


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

    if response is not None:
        return jsonify(response)

    return Response("Invalid specie name", status=400)


def get_specie_model_information(specie_name, model):
    """
    Handle fetching specified model information for specie
    """
    return specie_name + "_" + model


def predict_specie_with_model(specie_name, model):
    """
    Predict specie occurrence using specified model
    Date format
    """

    try:
        date_from_datetime = datetime.strptime(request.args.get("from"), '%Y-%m-%d')
        date_to_datetime = datetime.strptime(request.args.get("to"), '%Y-%m-%d')

        # Check if dates are correct
        if date_from_datetime > date_to_datetime:
            return Response("Invalid data range, (from after to)", status=400)

        response = app_service.predict_specie_with_model(specie_name, model, date_from_datetime, date_to_datetime)

        if response is not None:
            return jsonify(response)

        return Response("Invalid specie name", status=400)
    except ValueError:
        return Response("Invalid date format, try using YYYY-MM-DD", status=400)
