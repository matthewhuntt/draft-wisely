

import urllib.request
import json
import time
import pandas as pd


# league_id = "512935492240711680"
# try:
# 	with urllib.request.urlopen("https://api.sleeper.app/v1/draft/" + "512935492240711681" + "/picks") as url:
# 		draft = json.loads(url.read().decode())


with open("LeagueList.txt") as f:
	league_list = f.read().split('\n')

for i in range(len(league_list)):
	if league_list[i] == "512935492240711680":
		print(i)

