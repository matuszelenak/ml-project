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

def get_stats(player):
	url = "https://en.wot-life.com/eu/player/" + player
	s = requests.get(url).text
	soup = BeautifulSoup(s, 'html.parser')
	tank_table = soup.find('table', {'id' : 'tanks'})
	res = []
	for row in tank_table.find_all('tr')[1:]:
		res.append(row.find_all('td')[2].text.strip())
	return res

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

X = [0,4,87,9,2,4,6,52,7,8]
block_size = 2
for i in range(5):
	X_frac = X[:i*block_size] + X[(i+1)*block_size:]
	print(X_frac)

"""
temp = {}
i = 0
for filename in os.listdir("./replay_jsons"):
	f = open(os.path.join("./replay_jsons" , filename), 'r')
	j = json.loads("".join(f.readlines()))
	f.close()


	f = open(os.path.join("./replays_simple" , filename), 'r+')
	l = json.loads("".join(f.readlines()))

	l['map']['mode'] = j['GameMode']["Name"]

	f.seek(0)
	f.write(json.dumps(l, indent=4, sort_keys=True, ensure_ascii=False))
	f.truncate()
	f.close()
	i += 1
	update_progress(i, len(os.listdir("./replay_jsons")))
print(temp)
"""

"""
i = 0
for filename in os.listdir("./replay_jsons"):
	f = open(os.path.join("./replays_simple" , filename), 'r+')
	j = json.loads("".join(f.readlines()))

	if j['teams'][0]['team_id'] == j['subject']['team']:
		j['teams'][0]['spawn'] = j['map']['spawn']
		j['teams'][1]['spawn'] = inv_spawn[j['map']['spawn']]
	else:
		j['teams'][1]['spawn'] = j['map']['spawn']
		j['teams'][0]['spawn'] = inv_spawn[j['map']['spawn']]	

	del(j['map']['spawn'])

	f.seek(0)
	f.write(json.dumps(j, indent=4, sort_keys=True, ensure_ascii=False))
	f.truncate()
	f.close()
	i += 1
	update_progress(i, len(os.listdir("./replay_jsons")))
"""

i = 0
avg_incorrect_diff, avg_correct_diff = 0, 0
for filename in os.listdir("./replays_simple"):
	i += 1
	f = open(os.path.join("./replays_simple/" , filename), 'r')
	j = json.loads("".join(f.readlines()))
	f.close()

	#if (j['result']['reason'] != 'All vehicles destroyed'):
	#	continue
	if (j['result']['winner'] == 0):
		continue

	map_wr = maps[j['map']['name']][j['map']['mode']]
	winner = j['result']['winner']
	temp = []

	acc = 0
	for p in j['teams'][0]['players']:
		acc += p['tank_stats']['winrate'] * vba[unidecode(p['tank']['name'])]
	acc *= (1 + (map_wr[j['teams'][0]['spawn']] - 50)/100)
	temp.append([acc, j['teams'][0]['team_id']])
	acc = 0
	for p in j['teams'][1]['players']:
		acc += p['tank_stats']['winrate'] * vba[unidecode(p['tank']['name'])]
	temp.append([acc, j['teams'][1]['team_id']])

	
	#temp.append([sum([p['tank_stats']['WN8'] * p['tank_stats']['winrate'] * vba[unidecode(p['tank']['name'])] for p in j['teams'][0]['players']]), j['teams'][0]['team_id']])
	#temp.append([sum([p['tank_stats']['WN8'] * p['tank_stats']['winrate'] * vba[unidecode(p['tank']['name'])] for p in j['teams'][1]['players']]), j['teams'][1]['team_id']])

	"""
	
	for team, i in zip(j['teams'], [0,1]):
		if team['team_id'] == j['subject']['team']:
			wrs = maps[j['map']['name']][j['map']['mode']]
			temp[i][0] *= 1 + ((wrs[j['map']['spawn']] - wrs[inv[j['map']['spawn']]]) / 100)
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



"""
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
"""
