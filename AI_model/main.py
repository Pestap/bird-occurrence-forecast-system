#model = Sequential()
#model.add(Dense(4, input_dim=x_train.shape[1]))
#model.add(Dense(8))
#model.add(Dense(15))
#model.add(Dense(3))
#model.add(Dense(1))
#x_train, x_test, y_train, y_test = create_sets(0.1)
#optimizer = keras.optimizers.Adam(learning_rate=0.001)

#model.compile(
#    loss='mean_squared_error',
#    optimizer=optimizer,
#    metrics= 'mean_absolute_error'
#)

#es = EarlyStopping(monitor='loss', mode='min', patience=1000, restore_best_weights=True)

#history = model.fit(x_train, y_train, epochs=10, batch_size=75, callbacks=es)

#scores = model.evaluate(x_test, y_test, verbose=0)

#y_predict = model.predict(x_test)

#y_test_array = y_test.values

#df2 = pd.DataFrame({'actual' : y_test_array, 'predicted' : y_predict})

#print(df2)


