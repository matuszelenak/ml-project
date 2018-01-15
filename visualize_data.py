#!/usr/bin/python3
from matplotlib import pyplot as plt
import argparse
import json
from functools import reduce
import numpy as np

#Count the games where the net was confident over some treshold
def count_over_treshold(data, treshold):
	i = 0
	while i < len(data) and data[i][0] < treshold:		#too lazy to code binary search
		i+=1
	return reduce(lambda acc, x : acc + 1 if x[1] == 'True' else acc, data[:i], 0)

#For intervals of win chances, calculate the actual fraction of won games according to the pgreeniction
def accuracy_per_interval(data, step):
	bins = []
	result = [[], []]
	for win_chance in range(0,50, step):
		found, total = 0, 0
		for r in data:
			if  (win_chance < r['confidence'][0]*100 and r['confidence'][0]*100 < win_chance + step):
				total = total + 1
				if r['correct'] == 'False':
					found = found + 1
		if total > 5:
			result[0].append((2*win_chance+step)/2)
			result[1].append(found/total)

	for win_chance in range(50,100, step):
		found, total = 0, 0
		bins.append([0,0])
		for r in data:
			if  (win_chance < r['confidence'][0]*100 and r['confidence'][0]*100 < win_chance + step):
				total = total + 1
				if r['correct'] == 'True':
					found = found + 1
		if total > 5:
			result[0].append((2*win_chance+step)/2)
			result[1].append(found/total)

	return result

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str)

args = parser.parse_args()

f = open('{0}results.json'.format(args.path), 'r')
R = json.loads("".join(f.readlines()))
f.close()

f = open('{0}results_xvm.json'.format(args.path), 'r')
R_xvm = json.loads("".join(f.readlines()))
f.close()

f = open('{0}outliers.json'.format(args.path), 'r')
O = json.loads("".join(f.readlines()))
f.close()


f = open('{0}outliers_xvm.json'.format(args.path), 'r')
O_xvm = json.loads("".join(f.readlines()))
f.close()

print(len(O), len(O_xvm))


plt.figure()
plt.hist([o[0] for o in O], bins = 30, color = 'green', alpha=0.5, label = 'Our method')
plt.hist([o[0] for o in O_xvm], bins = 30, color = 'blue', alpha=0.5, label = 'XVM')
plt.title("Outlier distribution")
plt.legend(loc='upper right')
plt.xlabel("Confidence disparity")
plt.ylabel("Frequency")
plt.show()

#Relation between win chance prediction and truth
bins = accuracy_per_interval(R, 10)
bins_xvm = accuracy_per_interval(R_xvm, 10)
plt.figure()
plt.title("Win chance relation")
plt.xlabel("Actual win chance")
plt.ylabel("Predicted win chance (or confidence)")
plt.scatter(bins[0], bins[1], color = 'green')
plt.plot(np.unique(bins[0]), np.poly1d(np.polyfit(bins[0], bins[1], 1))(np.unique(bins[0])), color = 'green', label = 'Our method')
plt.scatter(bins_xvm[0], bins_xvm[1], color = 'blue')
plt.plot(np.unique(bins_xvm[0]), np.poly1d(np.polyfit(bins_xvm[0], bins_xvm[1], 1))(np.unique(bins_xvm[0])), color = 'blue', label = 'XVM')
plt.legend(loc='upper left')
plt.show()

#Distribution of win chances
plt.figure()
plt.hist([r['confidence'][0] for r in R], bins = 30, color = 'green', alpha=0.5, label = 'Our method')
plt.hist([r['confidence'][0] for r in R_xvm], bins = 30, color = 'blue', alpha=0.5, label = 'XVM')
plt.title("Win chance distribution")
plt.legend(loc='upper right')
plt.xlabel("Win chance")
plt.ylabel("Frequency")
plt.show()

#accuracy in relation to confidence
R_t = [[max(row['confidence']), row['correct'], row['confidence']] for row in R]
R_t.sort()
R_t_xvm = [[max(row['confidence']), row['correct'], row['confidence']] for row in R_xvm]
R_t_xvm.sort()
X, Y = [], []
for conf in range(50, 100):
	X.append(conf)
	Y.append(count_over_treshold(R_t, conf / 100) / len(R_t))
X_xvm, Y_xvm = [], []
for conf in range(50, 100):
	X_xvm.append(conf)
	Y_xvm.append(count_over_treshold(R_t_xvm, conf / 100) / len(R_t_xvm))

plt.figure()
plt.xlabel("Confidence")
plt.ylabel("Test accuracy")
plt.plot(X, Y, color = 'green', label = 'Our method')
plt.plot(X_xvm, Y_xvm, color = 'blue', label = 'XVM')
plt.legend(loc='lower right')
plt.show()


