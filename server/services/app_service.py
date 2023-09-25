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