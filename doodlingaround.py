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

#get_tank_stats("Whiskas_GJH", "T-10")

type_table = {"Medium Tank" : 1, "Heavy Tank" : 1, "Light Tank" : 1, "Tank Destroyer" : 1, "SPG" : 1}
n = {"USSR" : 1, 'France' : 1, 'USA' : 1, 'Sweden' : 1, 'Japan' : 1, 'Germany' : 1, 'United Kingdom' : 1, 'China' : 1, 'Czechoslovakia' : 1, 'Poland' : 1}
correct, total = 0, 0
t = len(os.listdir("./replays_simple"))
i = 0

avg_incorrect_diff, avg_correct_diff = 0, 0
for filename in os.listdir("./replays_simple"):
	i += 1
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))
	f.close()

	if (j['result']['reason'] != 'All vehicles destroyed'):
		continue
	if (j['result']['winner'] == 0):
		continue

	winner = j['result']['winner']
	temp = []

	
	temp.append([sum([n[p['tank']['nation']] * p['tank_stats']['winrate'] * vba[unidecode(p['tank']['name'])] for p in j['teams'][0]['players']]), j['teams'][0]['team_id']])
	temp.append([sum([n[p['tank']['nation']] * p['tank_stats']['winrate'] * vba[unidecode(p['tank']['name'])] for p in j['teams'][1]['players']]), j['teams'][1]['team_id']])

	"""
	for team, i in zip(j['teams'], [0,1]):
		if team['team_id'] == j['subject']['team']:
			temp[i][0] *= (maps[j['map']['name']][j['map']['spawn']] / 50)
	"""

	temp.sort(reverse = True)

	if temp[0][1] == winner:
		correct += 1
		#print(abs(int(temp[0][0]) - int(temp[1][0])), "Correct")
		avg_correct_diff += abs(int(temp[0][0]) - int(temp[1][0]))
	else:
		#print(abs(int(temp[0][0]) - int(temp[1][0])), "Incorrect")
		avg_incorrect_diff += abs(int(temp[0][0]) - int(temp[1][0]))



	total += 1

print("Prediction accuracy {0}%".format(correct / total))
print("Average rating diff for incorrect {0}".format(avg_incorrect_diff / (total - correct)))
print("Average rating diff for correct {0}".format(avg_correct_diff / correct))




tanks_encountered = {}
maps_encountered = {}
for filename in os.listdir("./replays_simple"):
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))
	f.close()
	maps_encountered[j['map']['name']] = True
	for p in j['teams'][0]['players'] + j['teams'][1]['players']:
		tank_name = p['tank']['name']
		tanks_encountered[tank_name] = True

for tank, _ in tanks_encountered.items():
	if not unidecode(tank) in vba:
		print("{0} not found!".format(tank))

for m, _ in maps_encountered.items():
	if not m in maps:
		print("{0} not found!".format(m))

tag_trans = {'o' : 'open', 'c' : 'city', 's' : 'small', 'l' : 'large', 'co' : 'corridor'}
for m in maps:
	print(m)
	tags = []
	for tag in input().split():
		tags.append(tag_trans[tag])
	maps[m]['tags'] = tags


f = open("./map_data.json", 'w')
f.write(json.dumps(maps, indent=4, sort_keys=True, ensure_ascii=False))
f.close()
