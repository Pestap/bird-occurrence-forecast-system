from entities.enums import Model as ModelType


class Model:
    def __init__(self, type, params):
        self.type = type
        self.params = params


class AutoregressionModel(Model):
    def __init__(self, params=None):
        if params is None:
            params = {
                "autoregression_order": {
                    "min": 0,
                    "max": 60,
                    "default": 24,
                }

            }
        super().__init__(ModelType.AUTOREGRESSION, params)


class ArmaModel(Model):
    def __init__(self, params=None):
        if params is None:
            params = {
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

        super().__init__(ModelType.ARMA, params)