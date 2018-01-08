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

f = open("./dataset.json", 'r')
data = json.loads("".join(f.readlines()))
f.close()

training_frac = 0.9
num_of_samples = int(len(data) * training_frac)


X = np.array([row[1:] for row in data])
Y = np.array([row[0] for row in data])

#print(X[:15])
#print(Y[:15])
"""
clf = svm.SVC()
clf.fit(X, Y)


correct, incorrect = 0, 0
test_samples = [row[1:] for row in data[num_of_samples::]]
test_results = [row[0] for row in data[num_of_samples::]]
for predicted, actual in zip(clf.predict(test_samples), test_results):
	if predicted == actual:
		correct += 1
	else:
		incorrect += 1

print(correct, incorrect)
"""


mlp = Sequential()
mlp.add(Dense(30, activation='tanh', input_dim=len(X[0])))
mlp.add(Dense(30, activation='tanh'))
mlp.add(Dense(2, activation='softmax'))

mlp.compile(loss='mse', optimizer=SGD(lr=0.4),  metrics=['accuracy'])

history = mlp.fit(X, to_categorical(Y), epochs=20, validation_split=0.3, verbose=True)

score = mlp.evaluate(X, to_categorical(Y))
print("\n\nloss: {} | train acc: {}".format(score[0], score[1]))