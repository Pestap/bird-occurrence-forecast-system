from prepare_data_set import *
from visualize_data import *

groups = create_groups()

dates, observations = prepare_observation_data(groups, 'województwo pomorskie')
draw_plot(dates, observations)







