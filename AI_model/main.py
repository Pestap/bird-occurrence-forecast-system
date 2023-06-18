from prepare_data_set import *
from visualize_data import *
from autoregression import *

groups = create_groups()

dates, observations = prepare_observation_data(groups, 'województwo wielkopolskie')

#train, test, predicted = boxcox_ar(dates, observations, 0.8)
train, test, predicted = autoreg( dates, observations, 0.98, 24)
#predicted = (predicted[0].rolling(2).sum(), predicted[1])


visualize_prediction_results(dates, train, test, predicted, 3)







