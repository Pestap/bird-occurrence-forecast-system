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


def draw_plot(json_data1, json_data2, state, title):
    p_dates1, p_values1 = get_series_from_json(json_data1['predictions'], state)
    t_dates1, t_values1 = get_series_from_json(json_data1['tests'], state)

    p_dates2, p_values2 = get_series_from_json(json_data2['predictions'], state)
    t_dates2, t_values2 = get_series_from_json(json_data2['tests'], state)

    fig, ax = plt.subplots()
    ax.plot(p_dates1, p_values1, label="Predictions (ar)", color='blue')
    ax.plot(t_dates1, t_values1, label="Test", color='green')
    ax.plot(p_dates2, p_values2, label="Predictions (arima)", color="red")
    plt.xticks(p_dates1[0::3], rotation=45)
    plt.grid(True)
    # TODO: update title with state
    legend=ax.legend(loc='upper right')
    plt.xlabel("Dates")
    plt.ylabel("Average observation count")
    plt.title(title)

    plt.show()

if __name__ == '__main__':
    base_url = "http://127.0.0.1:5000"

    model = "autoregression"
    specie = "motacilla_alba"
    from_date = "2021-01"
    to_date = "2023-01"
    ar_order = 24
    am_order = 12

    resource = f"api/birds/{specie}/models/{model}/predict?from={from_date}&to={to_date}&autoregression_order={ar_order}"
    #resource2 = f"api/birds/{specie}/models/arima/predict?from={from_date}&to={to_date}&autoregression_order={ar_order}&moving_average_order={am_order}&differencing_order=2&edge={edge}"
    #resource3 = f"api/birds/{specie}/models/arma/predict?from={from_date}&to={to_date}&autoregression_order={ar_order}&moving_average_order={am_order}&edge={edge}"
    #resource2 = f"api/birds/{specie}/models/autoregression/predict?from={from_date}&to={to_date}&autoregression_order={ar_order // 2}&edge={edge}"
    #resource2 = f"api/birds/{specie}/models/arma/predict?from={from_date}&to={to_date}&autoregression_order={ar_order}&moving_average_order={am_order}&edge={edge}"
    #resource2 = f"api/birds/{specie}/models/arma/predict?from={from_date}&to={to_date}&autoregression_order={ar_order}&moving_average_order={am_order}&edge={edge}"
    url = base_url + "/" + resource
    #url2 = base_url +"/" + resource2
    headers = {"Content-Type": "application/json; charset=utf-8"}
    #data={"autoregression_order": }

    data = {"autoregression_order": "24"}
    r = requests.get(url, headers=headers)


    #r2 = requests.get(url2, headers=headers)

    state = "wielkopolskie"
    print(r.reason)
    print(r.content)
    print(r.json()['custom_errors'])

   # x, y = get_series_from_json(r.json()['predictions'], state)

    draw_plot(r.json(), r.json(), state, "Autoreg vs arima")


