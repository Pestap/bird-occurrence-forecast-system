import keras.models
from keras import Sequential
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from sklearn import metrics
from tensorflow import keras
from prepare_data_set import *

model = Sequential()


x_train, x_test, y_train, y_test = create_sets(0.1)

model.add(Dense(4, input_dim=x_train.shape[1]))

model.add(Dense(30))
model.add(Dense(10))
model.add(Dense(1))

optimizer = keras.optimizers.Adam(learning_rate=0.001)

model.compile(
    loss='mean_squared_error',
    optimizer=optimizer,
    metrics= 'mean_absolute_error'
)

es = EarlyStopping(monitor='loss', mode='min', patience=1000, restore_best_weights=True)

history = model.fit(x_train, y_train, epochs=100, batch_size=50, callbacks=es)

scores = model.evaluate(x_test, y_test, verbose=0)

y_predict = model.predict(x_test)

y_test_array = y_test.values






