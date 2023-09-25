from server.models.enums import State


class AutoregressionModel:
    def __init__(self, state: State, months: int):
        self.state = state
        self.months = months

    def predict(self, observation_data, date_from, date_to):
        """
        observation_data - data from eBird, already prepared, regarding only
        one state, grouped by avg, month, used to predict next N months,
        N needs to be calculated based on last observation month and date_to

        If date_to is in observation_data, just return observation data


        Maybe add class DataPoint - Date, Value, Boolean for telling if point was predicted or not
        (or return a tuple) (date, value, T/F)

        Pseudocode

        if date_to is before last observation:
            return observations between from and to
        else
            make prediction to to
            return observations between from and to

        """


        pass
