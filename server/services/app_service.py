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
        return species[specie_name].make_predictions(model, date_from, date_to, model_params, edge_date)
    except KeyError:
        return None
