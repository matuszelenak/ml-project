#!/usr/bin/python3	

import json
import os

f = open('map_to_team_replays', 'r')
d = {}
for line in f.readlines():
	n, t = [x for x in line[:-1].strip().split('=')]
	d[n] = t
f.close()
res = {}
conv = {'1' : 2, '2' : 1}
for filename in os.listdir("./"):
	if not filename.endswith(".json"):
		continue
	f = open(filename, 'r')
	j = json.loads("".join(f.readlines()))
	map_name = j["Map"]["Name"]
	print(map_name)
	spawn = j["Map"]["Spawn"]
	winner_team = d[map_name]
	player_team = j['Player']['Team']
	actual_winner = int(j["Battle"]["WinnerTeam"])
	if (actual_winner == player_team):
		res[map_name] = {spawn : winner_team}
	else:
		res[map_name] = {spawn : conv[winner_team]}

print(res)