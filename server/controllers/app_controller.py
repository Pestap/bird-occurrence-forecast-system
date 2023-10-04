from datetime import datetime

from flask import Flask, request, jsonify, Response

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
    """
    Predict specie occurrence using specified model
    Date format

    {
        dolnoslaskie: {
            []
            []
        }.
        ...


        2011-11 : {
        dolnoslaskie: 212
        ..
        ,,
        ..


        }
    }
    """

    try:
        date_from_datetime = datetime.strptime(request.args.get("from"), '%Y-%m-%d')
        date_to_datetime = datetime.strptime(request.args.get("to"), '%Y-%m-%d')
        # Replace months with 1
        date_to_datetime = date_to_datetime.replace(day=1)
        date_from_datetime = date_from_datetime.replace(day=1)
        # Check if dates are correct
        if date_from_datetime > date_to_datetime:
            return Response("Invalid data range, (from after to)", status=400)

        response = app_service.predict_specie_with_model(specie_name, model, date_from_datetime, date_to_datetime)

        if response is not None:
            # Translate dates and round to 2 decimal places
            response_translated = {f"{date.year}-{date.month:0>{2}}": {state: round(observation_value, 2) for state, observation_value in value.items()} for date, value in response.items()}

            return jsonify(response_translated)

        return Response("Invalid specie name", status=400)
    except ValueError:
        return Response("Invalid date format, try using YYYY-MM-DD", status=400)

    # 2012-09-01
