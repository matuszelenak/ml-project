#!/usr/bin/python3	

import json
import os
import math
from bs4 import BeautifulSoup
import requests
import re

def update_progress(progress, total):
    print("\rProgress: [{0:50s}] {1:.1f}%".format('#' * int(progress/total * 50), progress/total*100), end="", flush=True)

url = "http://www.vbaddict.net/statistics_maps.php?groupby=3&fieldname=won_lost_ratio"
s = requests.get(url).text
soup = BeautifulSoup(s, 'html.parser')
maps = [row.find_all('td')[1].text.strip('\n').split('\n') + [re.sub(r'\s', '', row.find_all('td')[-1].text)] for row in soup.find('table', id = 'table-map-statistics').find_all('tr')[1:]]
spawn = {"Team 2" : "B", "Team 1" : "A"}
map_dict = {}
for m in maps:
	if m[0] not in map_dict:
		map_dict[m[0]] = {}
	map_dict[m[0]][spawn[m[1]]] = float(m[2][:-1])
f = open('./map_data.json', 'w')
f.write(json.dumps(map_dict, indent=4, sort_keys=True, ensure_ascii=False))
f.close()

t_rows = []
for tier in range(1,11):
	for  typ in range(1,6):
		url = "http://www.vbaddict.net/statistics.php?tier="+str(tier)+"&tanktype="+str(typ)+"&nation=0&battles=1&groupby=0&fieldname=won_lost_ratio&server=eu"
		s = requests.get(url).text
		soup = BeautifulSoup(s, 'html.parser')
		t_rows += soup.find('table', id = 'table-statistics').find_all('tr')[1:]
#print(t_rows)
tank_dict = {}
for row in t_rows:
	if (row.find_all('td')[1].find('a') == None):
		print(row)
		continue
	name = row.find_all('td')[1].find('a').text
	wr = float(re.sub(r'\s', '', row.find_all('td')[-1].text)[:-1])
	tank_dict[name] = wr
f = open('./tank_data.json', 'w')
f.write(json.dumps(tank_dict, indent=4, sort_keys=True, ensure_ascii=False))
f.close()