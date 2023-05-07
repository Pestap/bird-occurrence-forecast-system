import keras.models
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from sklearn import metrics
from tensorflow import keras

from preapre_ml_sets import create_sets




x_train, x_test, y_train, y_test = create_sets(0.2)