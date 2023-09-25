from server.models.species.ardea_alba import ArdeaAlba
from server.models.species.ciconia_ciconia import CiconiaCiconia

# species dictionary
species = {
    'ardea_alba': ArdeaAlba(),
    'ciconia_ciconia': CiconiaCiconia()
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


def predict_specie_with_model(specie_name, model, date_from, date_to):
    try:
        return species[specie_name].predict(model, date_from, date_to)
    except KeyError:
        return None
