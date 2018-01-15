#!/usr/bin/python3
import json
import argparse

def player_weight(player):
	W_wr = (100 + player['general_stats']['winrate'] - 48.5) / 100
	W_battles = 0
	if player['general_stats']['battles'] <= 500:
		W_battles = 0
	elif player['general_stats']['battles'] <= 5000:
		W_battles = (player['general_stats']['battles'] - 500)/10000
	elif player['general_stats']['battles'] <= 10000:
		W_battles = 0.45 + (player['general_stats']['battles'] - 5000) / 20000
	elif player['general_stats']['battles'] <= 20000:
		W_battles = 0.7 + (player['general_stats']['battles'] - 10000) / 40000
	else:
		W_battles = 0.95 + (player['general_stats']['battles'] - 20000) / 80000
	return player['general_stats']['WN8'] * W_wr * (W_wr + W_battles) * (W_wr + 0.25 * player['tank']['tier'])

def team_weight(team):
	return sum([player_weight(p) for p in team['players']])

parser = argparse.ArgumentParser()
parser.add_argument('path', type=str)

args = parser.parse_args()

f = open("{0}/results.json".format(args.path), 'r')
R = json.loads("".join(f.readlines()))
f.close()
print(len(R))

R_xvm = []

correct, total = 0, 0
O_xvm = []
for row in R:
	f = open("./replays_simple/{0}".format(row['label']), 'r')
	#print(row['label'])
	j = json.loads("".join(f.readlines()))
	f.close()
	A = team_weight(j['teams'][0])
	B = team_weight(j['teams'][1])
	WC = max(0.05, min(0.95, 0.5 + ((A/15)/(A/15 + B/15) - 0.5)*1.5))
	#print(WC)
	c = False
	if WC > 0.5:
		if j['result']['winner'] == j['teams'][0]['team_id']:
			correct += 1
			c = True
		else:
			O_xvm.append([abs(WC - (1 - WC)), row['label']])
	else:
		if j['result']['winner'] != j['teams'][0]['team_id']:
			correct += 1
			c = True
		else:
			O_xvm.append([abs(WC - (1 - WC)), row['label']])
	total += 1
	R_xvm.append({'confidence' : [WC, 1 - WC], 'correct' : str(c), "label" : row['label']})
O_xvm.sort(reverse = True)

f = open("{0}/results_xvm.json".format(args.path), 'w')
f.write(json.dumps(R_xvm, indent=4, sort_keys=True, ensure_ascii=False))
f.close()

f = open("{0}/outliers_xvm.json".format(args.path), 'w')
f.write(json.dumps(O_xvm, indent=4, sort_keys=True, ensure_ascii=False))
f.close()

print(correct/total)