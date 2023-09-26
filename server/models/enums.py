from enum import Enum


def translate_state_to_enum(state_name):
    if state_name == 'województwo dolnośląskie':
        return State.DOLNOSLASKIE
    elif state_name == 'województwo kujawsko-pomorskie':
        return State.KUJAWSKO_POMORSKIE
    elif state_name == 'województwo lubelskie':
        return State.LUBELSKIE
    elif state_name == 'województwo lubuskie':
        return State.LUBUSKIE
    elif state_name == 'województwo łódzkie':
        return State.LODZKIE
    elif state_name == 'województwo małopolskie':
        return State.MALOPOLSKIE
    elif state_name == 'województwo mazowieckie':
        return State.MAZOWIECKIE
    elif state_name == 'województwo opolskie':
        return State.OPOLSKIE
    elif state_name == 'województwo podkarpackie':
        return State.PODKARPACKIE
    elif state_name == 'województwo podlaskie':
        return State.PODLASKIE
    elif state_name == 'województwo pomorskie':
        return State.POMORSKIE
    elif state_name == 'województwo śląskie':
        return State.SLASKIE
    elif state_name == 'województwo świętokrzyskie':
        return State.SWIETOKRZYSKIE
    elif state_name == 'województwo warmińsko-mazurskie':
        return State.WARMINSKO_MAZURSKIE
    elif state_name == 'województwo wielkopolskie':
        return State.WIELKOPOLSKIE
    elif state_name == 'województwo zachodniopomorskie':
        return State.ZACHODNIOPOMORSKIE
    else:
        return None


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
    NEURAL_NETWORK = 2
