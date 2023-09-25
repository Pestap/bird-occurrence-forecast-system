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
    return jsonify(app_service.get_specie_info(specie_name))


def get_specie_available_models(specie_name):
    """
    Handle fetching available models
    """
    return jsonify(app_service.get_specie_models(specie_name))


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

    date_from_datetime = datetime.strptime(request.args.get("from"), '%Y-%m-%d')
    date_to_datetime = datetime.strptime(request.args.get("to"), '%Y-%m-%d')

    if date_from_datetime > date_to_datetime:
        return Response("Invalid data range", status=400)


    return jsonify(app_service.predict_specie_with_model(specie_name, model, date_from_datetime, date_to_datetime))
