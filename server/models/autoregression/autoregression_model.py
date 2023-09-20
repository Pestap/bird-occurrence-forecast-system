from server.models.enums import State


class AutoregressionModel:
    def __init__(self, state: State, months: int):
        self.state = state
        self.months = months

