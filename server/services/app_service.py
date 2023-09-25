from datetime import datetime

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
    return species[specie_name].get_info()


def get_specie_models(specie_name):
    print(species[specie_name].get_available_models())
    return species[specie_name].get_available_models()


def predict_specie_with_model(specie_name, model, date_from, date_to):
    date_from_datetime = datetime.strptime(date_from, '%Y-%m-%d')
    date_to_datetime = datetime.strptime(date_to, '%Y-%m-%d')

    if date_from_datetime.time() > date_to_datetime.time():
        return '400' # bad request

    return species[specie_name].predict(model, date_from, date_to)

