import entities.enums
from entities.enums import Model as ModelType
"""
Module for handling models with default parameters
"""


def get_model_params(model_name):
    if model_name.upper() == entities.enums.Model.ARMA.name:
        return ArmaModel.default_params
    elif model_name.upper() == entities.enums.Model.AUTOREGRESSION.name:
        return AutoregressionModel.default_params
    elif model_name.upper() == entities.enums.Model.ARIMA.name:
        return ArimaModel.default_params
    else:
        return None


class Model:
    def __init__(self, type, params):
        self.type = type
        self.params = params

    def to_json(self):
        return {"value": self.type.name.lower(), "display": self.pl_name}


class AutoregressionModel(Model):

    default_params = {
                "autoregression_order": {
                    "en_name": "Autoregression order",
                    "pl_name": "Rząd autoregresji",
                    "min": 0,
                    "max": 60,
                    "default": 24,
                }

            }

    def __init__(self, params=None):
        if params is None:
            params = AutoregressionModel.default_params
        self.pl_name = "Autoregresja"
        self.en_name = "Autoregression"
        super().__init__(ModelType.AUTOREGRESSION, params)


class ArmaModel(Model):
    default_params = {
                "autoregression_order": {
                    "en_name": "Autoregression order",
                    "pl_name": "Rząd autoregresji",
                    "min": 0,
                    "max": 60,
                    "default": 24,
                },
                "moving_average_order": {
                    "en_name": "Moving average order",
                    "pl_name": "Rząd średniej kroczącej",
                    "min": 0,
                    "max": 60,
                    "default": 24,
                }
            }

    def __init__(self, params=None):
        if params is None:
            params = ArmaModel.default_params
        self.pl_name = "ARMA"
        self.en_name = "ARMA"
        super().__init__(ModelType.ARMA, params)


class ArimaModel(Model):
    default_params = {
                "autoregression_order": {
                    "en_name": "Autoregression order",
                    "pl_name": "Rząd autoregresji",
                    "min": 0,
                    "max": 60,
                    "default": 24,
                },
                "moving_average_order": {
                    "en_name": "Moving average order",
                    "pl_name": "Rząd średniej kroczącej",
                    "min": 0,
                    "max": 60,
                    "default": 24,
                },
                "differencing_order": {
                    "en_name": "Differencing",
                    "pl_name": "Rząd różnicowania",
                    "min": 0,
                    "max": 60,
                    "default": 2,
                }
            }

    def __init__(self, params=None):
        if params is None:
            params = ArimaModel.default_params
        self.pl_name = "ARIMA"
        self.en_name = "ARIMA"
        super().__init__(ModelType.ARIMA, params)


class SarimaModel(Model):
    default_params = {
                "autoregression_order": {
                    "min": 0,
                    "max": 60,
                    "default": 24,
                },
                "moving_average_order": {
                    "min": 0,
                    "max": 60,
                    "default": 24,
                },
                "differencing_order": {
                    "min": 0,
                    "max": 60,
                    "default": 2,
                },
                "seasonal_autoregression_order": {
                    "min": 0,
                    "max": 60,
                    "default": 2,
                },
                "seasonal_moving_average_order": {
                    "min": 0,
                    "max": 60,
                    "default": 2,
                },
                "seasonal_differencing_order": {
                    "min": 0,
                    "max": 60,
                    "default": 2,
                },
                "periodicity": {
                    "min": 0,
                    "max": 60,
                    "default": 12,
                }

            }

    def __init__(self, params=None):
        if params is None:
            params = SarimaModel.default_params
        self.pl_name = "SARIMA"
        self.en_name = "SARIMA"
        super().__init__(ModelType.SARIMA, params)