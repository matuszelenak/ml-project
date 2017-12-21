import json
import os

myname = "Whiskas_GJH"

for filename in os.listdir("./replay_jsons"):
	print(os.path.join("./replay_jsons/" , filename))
	f = open(os.path.join("./replay_jsons/" , filename), 'r+')
	j = json.loads("".join(f.readlines()))
	#for key, value in j.items():
	#		print(key)
	t1, t2 = 0,0
	for member in j['Team01']:
		if not member['IsAlive']:
			t2 += 1
	for member in j['Team02']:
		if not member['IsAlive']:
			t1 += 1

	print("Final score : {0}! {1} : {2}".format(j["Result"]["Name"],t1,t2))

	for m1 in j['Team01'] + j["Team02"]:
		print(m1["Name"], m1["Tank"]["Name_Tank_Short"], int(m1["DamageOut"]["Damage"]))
	"""
	f.seek(0)
	f.write(json.dumps(j, indent=4, sort_keys=True, ensure_ascii=False))
	f.truncate()
	"""
	f.close()