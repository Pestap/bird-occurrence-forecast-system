import math
import numpy as np
import pandas as pd
import statsmodels as statsmodels
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from statsmodels.tsa.ar_model import AutoReg, ar_select_order

def boxcox_ar(dates, observations, split):

    for i in range(len(observations)):
        observations.loc[i] += 1

    ob_boxcox, lam = boxcox(observations)
    ob_stationary = np.diff(ob_boxcox)
    # np_diff ucina ostatnie
    split_index = math.floor(split * observations.shape[0])
    ob_stationary = pd.Series(ob_stationary)
    ob_boxcox_series = pd.Series(ob_boxcox)
    ob_boxcox_series_train = ob_boxcox_series.iloc[:split_index]

    (train_group, train_group_dates), (test_group, test_group_dates), (predicted, test_group_dates) = autoreg(dates, ob_stationary, split)

    boxcox_forecasts = []
    boxcox_tests = []
    for idx in range(len(predicted)):
        if idx == 0:
            boxcox_forecast = predicted[idx] + ob_boxcox_series_train.iloc[-1]
            boxcox_test = test_group[idx] + ob_boxcox_series_train.iloc[-1]
        else:
            boxcox_forecast = predicted[idx] + boxcox_forecasts[idx - 1]
            boxcox_test = test_group[idx] + boxcox_tests[idx - 1]

        boxcox_forecasts.append(boxcox_forecast)
        boxcox_tests.append(boxcox_test)

    forecast = pd.Series(inv_boxcox(boxcox_forecasts, lam))
    test = pd.Series(inv_boxcox(boxcox_tests, lam))

    train = pd.Series(observations.iloc[:split_index])
    train.reset_index(inplace=True, drop=True)
    for i in range(len(forecast)):
        forecast.loc[i] -= 1

        test.loc[i] -= 1

    for i in range(len(train)):
        train.loc[i] -= 1

    return (train, train_group_dates), (test, test_group_dates[:-1]), (forecast, test_group_dates[:-1])

def autoreg(dates, group, split, lags=24):

    group_df_len = group.shape[0]
    split_index = math.floor(split * group_df_len)

    train_group = group.iloc[:split_index]
    train_group_dates = dates.iloc[:split_index]
    test_group = group.iloc[split_index:]
    test_group_dates = dates.iloc[split_index:]

    selector = ar_select_order(train_group, 12)
    model = AutoReg(train_group, lags=lags).fit()

    predicted = list(model.forecast(steps=test_group.shape[0]))
    train_group.reset_index(inplace=True, drop=True)
    train_group_dates.reset_index(inplace=True, drop=True)
    test_group.reset_index(inplace=True, drop=True)
    test_group_dates.reset_index(inplace=True, drop=True)
    predicted= pd.Series(predicted)

    # Handle negative values
    for i in range(len(predicted)):
        if predicted.loc[i] < 0:
            predicted.loc[i] = 0

    return (train_group, train_group_dates), (test_group, test_group_dates), (predicted, test_group_dates)