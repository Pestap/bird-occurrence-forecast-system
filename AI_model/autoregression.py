import math
import numpy as np
import pandas as pd
import statsmodels as statsmodels
from scipy.stats import boxcox
from scipy.special import inv_boxcox
from statsmodels.tsa.ar_model import AutoReg, ar_select_order
def autoreg(dates, group, split, lags=24):

    group_df_len = group.shape[0]
    split_index = math.floor(split * group_df_len)
    split_index = group_df_len - split - 1



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