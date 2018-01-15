#!/usr/bin/python3	

import json
import os
import math
from unidecode import unidecode
from functools import reduce
import numpy as np

f = open("./tank_data.json", 'r')
vba = json.loads("".join(f.readlines()))
f.close()

f = open("./map_data.json", 'r')
maps = json.loads("".join(f.readlines()))
f.close()

X = []
Y = []
labels = []
category_index = {"Heavy Tank" : 0, "Medium Tank": 1, "Tank Destroyer" : 2, "Light Tank" : 3, "SPG" : 4}
params = 3

def get_strength(team):
	vector = [[[0 for _ in range(params)] for _ in range(5)] for _ in range(3)]
	mintier = reduce(lambda acc, x : min(x['tank']['tier'], acc), team ,10)
	for p in team:
		ri = p['tank']['tier'] - mintier
		ci = category_index[p['tank']['category']]
		vector[ri][ci][0] =	vector[ri][ci][0] + vba[unidecode(p['tank']['name'])]
		vector[ri][ci][1] =	vector[ri][ci][1] + p['tank_stats']['winrate']
		vector[ri][ci][2] =	vector[ri][ci][2] + p['general_stats']['winrate']
	return vector

def create_data_row(j, sgn):
	first_strength = np.array(get_strength(j['teams'][(sgn)%2]['players']))
	second_strength = np.array(get_strength(j['teams'][(sgn+1)%2]['players']))
	first_strength = first_strength.reshape((3*5*params))
	second_strength = second_strength.reshape((3*5*params))
	first_strength = np.append(first_strength, [maps[j['map']['name']][j['map']['mode']][j['teams'][sgn%2]['spawn']]])
	second_strength = np.append(second_strength, [maps[j['map']['name']][j['map']['mode']][j['teams'][(sgn + 1) %2]['spawn']]])
	strength_diff = first_strength - second_strength
	strength_diff = np.around(strength_diff, decimals = 3)
	return strength_diff.tolist()

for filename in os.listdir("./replays_simple"):
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))

	if (j['result']['winner'] == 0):
		continue

	X.append(create_data_row(j, 0))
	X.append(create_data_row(j, 1))

	if j['teams'][0]['team_id'] ==  j['result']['winner']:
		Y += [1, 0]
	else:
		Y += [0, 1]

	labels.append(filename)
	labels.append(filename)


f_s = open("./datasets/dataset_v2_X.json", 'w')
f_s.write(json.dumps(X, indent = 4))
f_s.close()

f_s = open("./datasets/dataset_v2_Y.json", 'w')
f_s.write(json.dumps(Y, indent = 4))
f_s.close()

f_s = open("./datasets/dataset_v2_labels.json", 'w')
f_s.write(json.dumps(labels, indent = 4))
f_s.close()