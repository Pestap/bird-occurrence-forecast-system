from enum import Enum


class State(Enum):
    DOLNOSLASKIE = 1
    KUJAWSKO_POMORSKIE = 2
    LUBELSKIE = 3
    LUBUSKIE = 4
    LODZKIE = 5
    MALOPOLSKIE = 6
    MAZOWIECKIE = 7
    OPOLSKIE = 8
    PODKARPACKIE = 9
    PODLASKIE = 10
    POMORSKIE = 11
    SLASKIE = 12
    SWIETOKRZYSKIE = 13
    WARMINSKO_MAZURSKIE = 14
    WIELKOPOLSKIE = 15
    ZACHODNIOPOMORSKIE = 16


class Model(Enum):
    AUTOREGRESSION = 1
    ARMA = 2
    ARIMA = 3
    SARIMA = 4
    NEURAL_NETWORK = 5


state_translation_dictionary = {
    State.DOLNOSLASKIE: 'województwo dolnośląskie',
    State.KUJAWSKO_POMORSKIE: 'województwo kujawsko-pomorskie',
    State.LUBELSKIE: 'województwo lubelskie',
    State.LUBUSKIE: 'województwo lubuskie',
    State.LODZKIE: 'województwo łódzkie',
    State.MALOPOLSKIE: 'województwo małopolskie',
    State.MAZOWIECKIE: 'województwo mazowieckie',
    State.OPOLSKIE: 'województwo opolskie',
    State.PODKARPACKIE: 'województwo podkarpackie',
    State.PODLASKIE: 'województwo podlaskie',
    State.POMORSKIE: 'województwo pomorskie',
    State.SLASKIE: 'województwo śląskie',
    State.SWIETOKRZYSKIE: 'województwo świętokrzyskie',
    State.WARMINSKO_MAZURSKIE: 'województwo warmińsko-mazurskie',
    State.WIELKOPOLSKIE: 'województwo wielkopolskie',
    State.ZACHODNIOPOMORSKIE: 'województwo zachodniopomorskie'
}


def translate_state_to_enum(state_name):
    position = list(state_translation_dictionary.values()).index(state_name)
    return list(state_translation_dictionary.keys())[position]


def translate_enum_to_state(state_enum_name):
    try:
        state_name = state_translation_dictionary[State[state_enum_name.upper()]]
        return state_name.split(" ")[-1]
    except KeyError:
        return ""
