from prepare_data_set import *
from visualize_data import *
from autoregression import *

groups = create_groups('../data/ciconia_ciconia.csv')


state = 'województwo wielkopolskie'
months = 36
dates, observations = prepare_observation_data(groups, state)

#train, test, predicted = boxcox_ar(dates, observations, 0.8)
train, test, predicted = autoreg( dates, observations, 12, months)
#predicted = (predicted[0].rolling(2).sum(), predicted[1])


visualize_prediction_results(dates, train, test, predicted, state, months, True, 3)



errors = []
for i in range(6, 48):
    train_i, test_i, predicted_i = autoreg(dates, observations, 24, i)

    mean_abs_error = 0

    for j in range(len(test_i[0])):
        mean_abs_error += abs(test_i[0][j] - predicted_i[0][j])

    errors.append((i, mean_abs_error / i))


for e in errors:
    print(f"{e[0]} ---> {e[1]}")






