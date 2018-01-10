#!/usr/bin/python3	

import json
import os
import math
from unidecode import unidecode
from functools import reduce

f = open("./tank_data.json", 'r')
vba = json.loads("".join(f.readlines()))
f.close()

X = []
Y = []
labels = []
category_index = {"Heavy Tank" : 0, "Medium Tank": 1, "Tank Destroyer" : 2, "Light Tank" : 3, "SPG" : 4}

def process_team(team, dp, sgn):
	mintier = reduce(lambda acc, x : min(x['tank']['tier'], acc), team ,10)
	for p in team:
		ri = p['tank']['tier'] - mintier
		ci = category_index[p['tank']['category']]
		dp[ri][ci][0] = dp[ri][ci][0] + sgn * int(vba[unidecode(p['tank']['name'])])
		dp[ri][ci][1] = dp[ri][ci][1] + sgn * int(p['tank_stats']['winrate'])
		dp[ri][ci][2] = dp[ri][ci][2] + sgn * p['general_stats']['winrate']
	return dp

for filename in os.listdir("./replays_simple"):
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))

	dp = [[[0,0,0] for _ in range(5)] for _ in range(3)]
	dp = process_team(j['teams'][0]['players'], dp, 1)
	dp = process_team(j['teams'][1]['players'], dp, -1)

	X.append(dp)

	dp = [[[0,0,0] for _ in range(5)] for _ in range(3)]
	dp = process_team(j['teams'][0]['players'], dp, -1)
	dp = process_team(j['teams'][1]['players'], dp, 1)
	X.append(dp)

	if j['teams'][0]['team_id'] ==  j['result']['winner']:
		Y += [1, 0]
	else:
		Y += [0, 1]

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