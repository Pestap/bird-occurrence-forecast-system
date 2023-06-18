from prepare_data_set import *
from visualize_data import *
from autoregression import *

groups = create_groups()

dates, observations = prepare_observation_data(groups, 'województwo pomorskie')

train, test, predicted = boxcox_ar(dates, observations, 0.95)
#train, test, predicted = autoreg( dates, observations, 0.95)

visualize_prediction_results(dates[1:], train, test, predicted)







