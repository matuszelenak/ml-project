#!/usr/bin/python3	

import json
import os
import math
from bs4 import BeautifulSoup
import requests
import re
from unidecode import unidecode

def update_progress(progress, total):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress/total * 50), progress/total*100), end="", flush=True)

f = open("./tank_data.json", 'r')
vba = json.loads("".join(f.readlines()))
f.close()

f = open("./map_data.json", 'r')
maps = json.loads("".join(f.readlines()))
f.close()

replace_dict = {"AMX M4 1949 Liberte" : "AMX M4 mle. 49 Liberte", 'Großtraktor - Krupp' : 'Grosstraktor - Krupp'}
inv_spawn = {"B" : "A", "A": "B"}
type_table = {"Medium Tank" : 1, "Heavy Tank" : 1, "Light Tank" : 1, "Tank Destroyer" : 1, "SPG" : 1}
n = {"USSR" : 1, 'France' : 1, 'USA' : 1, 'Sweden' : 1, 'Japan' : 1, 'Germany' : 1, 'United Kingdom' : 1, 'China' : 1, 'Czechoslovakia' : 1, 'Poland' : 1}
map_type = {"Medium Tank" : ["open"], "Heavy Tank" : ['city', 'corridor'], 'Light Tank' : ['open'], "Tank Destroyer" : ['open',], 'SPG' : ['open', 'large']}

correct, total = 0, 0
t = len(os.listdir("./replays_simple"))

i = 0
avg_incorrect_diff, avg_correct_diff = 0, 0
for filename in os.listdir("./replays_simple"):
	i += 1
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))
	f.close()

	if (j['result']['winner'] == 0):
		continue

	map_wr = maps[j['map']['name']][j['map']['mode']]
	winner = j['result']['winner']
	temp = []

	acc = 0
	for p in j['teams'][0]['players']:
		acc += p['tank_stats']['winrate'] + vba[unidecode(p['tank']['name'])] + p['general_stats']['winrate']
	acc *= (1 + (map_wr[j['teams'][0]['spawn']] - 50)/100)
	temp.append([acc, j['teams'][0]['team_id']])
	acc = 0
	for p in j['teams'][1]['players']:
		acc += p['tank_stats']['winrate'] + vba[unidecode(p['tank']['name'])] + p['general_stats']['winrate']
	temp.append([acc, j['teams'][1]['team_id']])

	temp.sort(reverse = True)

	if temp[0][1] == winner:
		correct += 1
		avg_correct_diff += abs(int(temp[0][0]) - int(temp[1][0]))
	else:
		avg_incorrect_diff += abs(int(temp[0][0]) - int(temp[1][0]))

	total += 1

print("Prediction accuracy {0}%".format(correct / total))
print("Average rating diff for incorrect {0}".format(avg_incorrect_diff / (total - correct)))
print("Average rating diff for correct {0}".format(avg_correct_diff / correct))
