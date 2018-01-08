#!/usr/bin/python3	

import json
import os
import math
from unidecode import unidecode

f = open("./tank_data.json", 'r')
vba = json.loads("".join(f.readlines()))
f.close()

data_matrix = []
for filename in os.listdir("./replays_simple"):
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))

	team1 = []
	for p in j['teams'][0]['players']:
		team1.append([p['tank']['tier'], p['tank']['category'], p['general_stats'], p['tank_stats'], p['tank']])
	team2 = []
	for p in j['teams'][1]['players']:
		team2.append([p['tank']['tier'], p['tank']['category'], p['general_stats'], p['tank_stats'], p['tank']])


	team1.sort(reverse = True, key=lambda x: (x[0], x[1]))
	team2.sort(reverse = True, key=lambda x: (x[0], x[1]))
	datarow = []
	for p1, p2 in zip(team1, team2):
		p1stat = int(p1[4]['tier'] * p1[3]['winrate'] * vba[unidecode(p1[4]['name'])])
		p2stat = int(p2[4]['tier'] * p2[3]['winrate'] * vba[unidecode(p2[4]['name'])])
		datarow.append(p1stat - p2stat)

	if j['teams'][0]['team_id'] ==  j['result']['winner']:
		datarow = [1] + datarow
	else:
		datarow = [0] + datarow
	data_matrix.append(datarow)

f_s = open("dataset.json", 'w')
f_s.write(json.dumps(data_matrix, indent = 4))
f_s.close()