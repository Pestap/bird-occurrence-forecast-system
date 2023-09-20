from flask import Flask, request

app = Flask(__name__)


def get_specie_info(specie_name):
    """
    Handle fetching specified specie information
    """
    return specie_name


def get_specie_available_models(specie_name):
    """
    Handle fetching available models
    """
    return specie_name +"_models"


def get_specie_model_information(specie_name, model):
    """
    Handle fetching specified model information for specie
    """
    return specie_name + "_" + model


def predict_specie_with_model(specie_name, model):
    """
    Predict specie occurrence using specified model
    """
    return specie_name + "_" + model +"_prediction"


if __name__ == '__main__':
    app.run(debug=True)


