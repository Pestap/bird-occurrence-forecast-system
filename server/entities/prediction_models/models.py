import entities.enums
from entities.enums import Model as ModelType


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


class AutoregressionModel(Model):
    default_params = {
                "autoregression_order": {
                    "min": 0,
                    "max": 60,
                    "default": 24,
                }

            }

    def __init__(self, params=None):
        if params is None:
            params = AutoregressionModel.default_params
        super().__init__(ModelType.AUTOREGRESSION, params)


class ArmaModel(Model):
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
                }
            }

    def __init__(self, params=None):
        if params is None:
            params = ArmaModel.default_params

        super().__init__(ModelType.ARMA, params)


class ArimaModel(Model):
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
                }
            }

    def __init__(self, params=None):
        if params is None:
            params = ArimaModel.default_params

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

        super().__init__(ModelType.SARIMA, params)