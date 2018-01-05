#!/usr/bin/python3

import json
import os
from bs4 import BeautifulSoup
import requests

subject_name = ""
subject_page = None

def update_progress(progress, total):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress/total * 50), progress/total*100), end="", flush=True)


def get_stats(player, tank):
	global subject
	global subject_page
	soup = None
	if player == subject_name and subject_page != None:
		soup = subject_page
	else:
		url = "https://en.wot-life.com/eu/player/" + player
		s = requests.get(url).text
		soup = BeautifulSoup(s, 'html.parser')
		if player == subject_name:
			subject_page = soup


	tank_table = soup.find('table', {'id' : 'tanks'})
	if (tank_table == None):
		print("Player {0} not found".format(player))
		return None
	stat_table = soup.find('table', {'class' : "stats-table table-md"})
	if (stat_table == None):
		print("Player {0} not found".format(player))
		return None
	stat_rows = stat_table.find_all('tr')

	results = {}
	results['WN8'] = int(stat_rows[-1].find_all('td')[0].text[:-3])
	results['battles'] = int(stat_rows[1].find_all('td')[0].text)
	results['WR'] = float(stat_rows[3].find_all('td')[1].text[:-1].replace(',', '.'))
	#print(stat_table)
	for row in tank_table.find_all('tr')[1:]:
		if row.find_all('td')[2].text.strip() == tank:
			results['t_WN8'] = int(row.find_all('td')[-1].text[:-3])
			results['t_WR'] = float(row.find_all('td')[-2].text[:-1].replace(',', '.'))
			results['t_DMG'] = int(row.find_all('td')[-5].text[:-3])
			results['t_battles'] = int(row.find_all('td')[-3].text)
			results['t_nation'] = row.find_all('td')[-7].find('span')['title']
			return results
	print("Tank {0} not found for player {1}".format(tank, player))
	return None

def convert_to_seconds(lifetime):
	h,m,s = lifetime.split(':')
	return int(m)*60 + int(s)

def process_team(j, id):
	team_members = []
	i = 0
	for player in j[id]:
		member = {"name" : player["Name"]}
		member["tank"] = {"name" : player["Tank"]["Name_Tank"], "tier": int(player["Tank"]["Info"]["Tier"]), "category": player["Tank"]["Info"]["ClassName"]}
		performance = {}
		performance["damage_dealt"] = int(player["DamageOut"]["Damage"])
		performance['assisted_dmg'] = int(player["DamageOut"]['Assist'])
		performance["survived"] = player['IsAlive']
		performance["lifetime"] = convert_to_seconds(player["LifeTime"])

		member["performance"] = performance
		s = get_stats(player['Name'], player["Tank"]["Name_Tank"])
		if (s == None):
			print()
			return None
		t_stats = {}
		t_stats['WN8'] = s['t_WN8']
		t_stats['winrate'] = s['t_WR']
		t_stats['damage'] = s['t_DMG']
		t_stats['battles'] = s['t_battles']
		member['tank_stats'] = t_stats
		member['tank']['nation'] = s['t_nation']
		stats = {}
		stats['WN8'] = s['WN8']
		stats['winrate'] = s['WR']
		stats['battles'] = s['battles']
		member['general_stats'] = stats
		team_members.append(member)
		i+=1
		update_progress(i, len(j[id]))
	return {"team_id" : int(j[id][0]["Team"]), "players" : team_members}

for filename in os.listdir("./replay_jsons")[800:]:
	if os.path.isfile(os.path.join("./replays_simple/" , filename)):
		continue
	f = open(os.path.join("./replay_jsons/" , filename), 'r')
	j = json.loads("".join(f.readlines()))

	if j["IsIncomplete"]:
		continue

	new_j = {"teams" : [], "subject" : {}, "result": {}}

	new_j["subject"]["name"] = j['Player']["Name"]
	new_j["subject"]["team"] = int(j['Player']["Team"])

	subject_name = j['Player']["Name"]

	new_j["map"] = {"name" : j["Map"]["Name"], "spawn" : j["Map"]["Spawn"]}
	print(filename)

	t1 = process_team(j, "Team01")
	if t1 == None:
		continue
	t2 = process_team(j, "Team02")
	if t2 == None:
		continue
	new_j["teams"] = [t1, t2]

	new_j["result"]["name"] = j["Result"]["Name"]
	new_j["result"]["reason"] = j["Result"]["Reason"]

	if "WinnerTeam" in j["Battle"]:
		new_j["result"]["winner"] = int(j["Battle"]["WinnerTeam"])
	else:
		new_j["result"]["winner"] = 0

	f_s = open(os.path.join("./replays_simple/" , filename), 'w')
	f_s.write(json.dumps(new_j, indent=4, sort_keys=True, ensure_ascii=False))
	f_s.close()