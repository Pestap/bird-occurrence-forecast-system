import json
from datetime import datetime

import requests
from matplotlib import pyplot as plt

from server.models.enums import State


def get_series_from_json(json_data, state):
    dates = []
    values = []
    for date, data in json_data.items():
        values.append(data[state.name])
        if data[state.name] is None:
            print("X")

        # Create date
        date_array = date.split("-")

        year = int(date_array[0])
        month_string = date_array[1]

        month = int(month_string[-1:]) if month_string[0] == '0' else int(month_string) # handle leading zeroes
        datetime_date = datetime(year, month, 1)

        dates.append(datetime_date)

    return dates, values


def draw_plot(x,y):
    plt.plot(x,y, label="Observations")
    plt.xticks(x[0::3], rotation=45)
    plt.vlines(x=datetime(2023,1,1), ymin = -10, ymax=10, colors = 'red', label= 'Observations - Predictions border')
    plt.grid(True)
    # TODO: update title with state
    plt.xlabel("Dates")
    plt.ylabel("Average observation count")
    plt.title("Obesrvations")
    plt.legend()
    plt.show()

if __name__ == '__main__':
    base_url = "http://127.0.0.1:5000"

    model = "autoregression"
    specie = "ciconia_ciconia"
    from_date = "2021-08-25"
    to_date = "2026-01-1"

    resource = f"api/birds/{specie}/models/{model}/predict?from={from_date}&to={to_date}"

    url = base_url + "/" + resource

    r = requests.get(url)


    state = State.POMORSKIE
    x, y = get_series_from_json(r.json(), state)

    draw_plot(x,y)
