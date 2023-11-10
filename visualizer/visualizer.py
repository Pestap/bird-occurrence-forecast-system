import json
from datetime import datetime

import requests
from matplotlib import pyplot as plt


def get_series_from_json(json_data, state):
    dates = []
    values = []
    for date, data in json_data.items():
        values.append(data[state])
        if data[state] is None:
            print("X")

        # Create date
        date_array = date.split("-")

        year = int(date_array[0])
        month_string = date_array[1]

        month = int(month_string[-1:]) if month_string[0] == '0' else int(month_string) # handle leading zeroes
        datetime_date = datetime(year, month, 1)

        dates.append(datetime_date)

    return dates, values


def draw_plot(json_data, state):
    p_dates, p_values = get_series_from_json(json_data['predictions'], state)
    t_dates, t_values = get_series_from_json(json_data['tests'], state)

    fig, ax = plt.subplots()
    ax.plot(p_dates, p_values, label="Predictions", color='blue')
    ax.plot(t_dates, t_values, label="Test", color='red')
    plt.xticks(p_dates[0::3], rotation=45)
    plt.grid(True)
    # TODO: update title with state
    legend=ax.legend(loc='center right')
    plt.xlabel("Dates")
    plt.ylabel("Average observation count")
    plt.title(f"Obesrvations - {state}")

    plt.show()

if __name__ == '__main__':
    base_url = "http://127.0.0.1:5000"

    model = "autoregression"
    specie = "grus_grus"
    from_date = "2005-01-01"
    to_date = "2028-01-1"
    ar_order = 24
    edge= edge="2021-12-01"
    resource = f"api/birds/{specie}/models/{model}/predict?from={from_date}&to={to_date}&autoregression_order={ar_order}&edge={edge}"

    url = base_url + "/" + resource

    headers = {"Content-Type": "application/json; charset=utf-8"}
    #data={"autoregression_order": }

    data = {"autoregression_order": "24"}
    r = requests.get(url, headers=headers)



    state = "wielkopolskie"
    print(r.reason)
    print(r.content)
    print(r.json()['mae_errors'])

   # x, y = get_series_from_json(r.json()['predictions'], state)

    draw_plot(r.json(), state)
