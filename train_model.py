#!/usr/bin/python3	

import json
import numpy as np
from matplotlib import pyplot as plt
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Activation, Flatten, MaxPooling2D
from keras.optimizers import SGD, Adam
from keras.utils import to_categorical
from keras import backend as K
from sklearn import svm
from keras.models import load_model

def normalize(X):
	return X - np.mean(X, axis = 0)

def train_models(X, Y, num):
	models = []
	block_size = len(X) // num
	for i in range(num):
		X_frac = np.array(X[:i*block_size] + X[(i+1)*block_size:])
		X_frac = X_frac.reshape((-1, 3*5*3))
		Y_frac = Y[:i*block_size] + Y[(i+1)*block_size:]
		X_val = np.array(X[i*block_size:(i+1)*block_size])
		X_val = X_val.reshape((-1, 3*5*3))
		Y_val = Y[i*block_size:(i+1)*block_size]
		mlp = Sequential()
		mlp.add(Dense(45, activation='tanh', input_dim=X_frac.shape[1]))
		mlp.add(Dense(45, activation='tanh'))
		mlp.add(Dense(15, activation='tanh'))
		mlp.add(Dense(2, activation='softmax'))
		mlp.compile( optimizer=Adam(0.04), loss='binary_crossentropy',  metrics=['accuracy'])

		history = mlp.fit(X_frac, to_categorical(Y_frac), epochs=20, validation_data = (X_val, to_categorical(Y_val)), verbose=True)
		models.append(mlp)
	return models

def evaluate(X, Y, models):
	f = open("outliers_indexes", 'w')
	X = np.array(X)
	X = X.reshape((-1, 3*5*3))
	pred_avg = np.zeros((X.shape[0], 2))
	for model in models:
		pred_avg += model.predict(X)
	pred_avg /= len(models)
	correct = 0
	outliers = []
	for predicted, result, index in zip(pred_avg, Y, range(len(Y))):
		if predicted[result] > predicted[(result + 1) % 2]:
			correct += 1
		else:
			print(predicted)
			if abs(predicted[0] - predicted[1] > 0.1):
				outliers.append(index)
		#print(predicted, result)
	f.write(str(outliers))
	f.close()
	print(correct, len(Y))

def save_models(path, models):
	for i in range(len(models)):
		models[0].save('{0}_part{1}.h5'.format(path, i+1))

def load_models(path, number):
	models = []
	for i in range(number):
		print('{0}_part{1}.h5'.format(path, i+1))
		models.append(load_model('{0}_part{1}.h5'.format(path, i+1)))
	return models

f = open("./datasets/dataset_v2_X.json", 'r')
X = json.loads("".join(f.readlines()))
f.close()

f = open("./datasets/dataset_v2_Y.json", 'r')
Y = json.loads("".join(f.readlines()))
f.close()

#nets = train_models(X, Y, 7)
nets = load_models('./models/model', 7)
print(nets)
#save_models('./models/model', nets)
evaluate(X, Y, nets)

for model, i in zip(nets,range(len(nets))):
	model.save('./models/model_part{0}.h5'.format(i+1))
"""
mlp = Sequential()
mlp.add(Dense(45, activation='tanh', input_dim=X.shape[1]))
mlp.add(Dense(45, activation='tanh'))
mlp.add(Dense(15, activation='tanh'))
mlp.add(Dense(2, activation='softmax'))

mlp.compile( optimizer=Adam(0.04), loss='binary_crossentropy',  metrics=['accuracy'])
		
print(mlp.output_shape)

history = mlp.fit(X, to_categorical(Y), epochs=20, validation_split=0.3, verbose=True)

score = mlp.evaluate(X, to_categorical(Y))
print("\n\nloss: {} | train acc: {}".format(score[0], score[1]))

if input() == "y":
	mlp.save('./models/model.h5')
	print("Model saved")

del(mlp)
"""

'''
plt.figure()
plt.plot(history.history['loss'], label='training loss')
plt.plot(history.history['val_loss'], label='validation loss')
plt.legend(loc='best')

plt.figure()
plt.plot(history.history['acc'], label='train accuracy')
plt.plot(history.history['val_acc'], label='validation accuracy')
plt.legend(loc='best')
plt.show()
'''