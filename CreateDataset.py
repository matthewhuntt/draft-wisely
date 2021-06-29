
"""
Fields:
user_id
league_id
round_1
round_2
...
round_17
scoring_settings (PPR, .5 PPR, 0 PPR)
roster_qb
roster_rb
roster_wr
roster_te
roster_flex
made_playoffs

Filtering:
1 QB leagues only
Redraft leagues only
10-12 team leagues only
"""

import urllib.request
import json
import time
import pandas as pd

#read in list of leagues
with open("LeagueList.txt") as f:
	league_list = f.read().split('\n')

def getDraft(league_id):
	"""
	Given a league_id, fetch all users in the league
	Return a list of all users
	"""

	#get draft_id using league_id, as well as the league settings
	time.sleep(.05)
	with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + league_id + "/drafts") as url:
	    draft = json.loads(url.read().decode())
	    draft_id = draft[0]['draft_id']
	    settings = draft[0]['settings']
	    settings['scoring_type'] = draft[0]['metadata']['scoring_type']
	    settings['season_type'] = draft[0]['season_type']
	
	#get all picks using draft_id
	time.sleep(.05)
	with urllib.request.urlopen("https://api.sleeper.app/v1/draft/" + draft_id + "/picks") as url:
	    picks = json.loads(url.read().decode())

	return(picks, settings)

def buildPickDict(picks):
	"""
	Take in list of all picks in draft
	Return a dictionary with user_ids as keys and all of users picks in a dictionary as values
	"""
	pick_dict = {}
	for pick in picks:
		if pick['picked_by'] != "":		#bots have empty strings for user_id
			if pick['picked_by'] in pick_dict.keys():
				pick_dict[pick['picked_by']][pick['round']] = pick['metadata']['position']
			else:
				pick_dict[pick['picked_by']] = {pick['round']: pick['metadata']['position']}



	return pick_dict

def getPlayoffs(user, league_id):
	"""
	"""
	time.sleep(.05)
	with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + league_id + "/winners_bracket") as url:
		bracket = json.loads(url.read().decode())

	playoff_team_set = set()
	for matchup in bracket:
		playoff_team_set.add(matchup['t1'])
		playoff_team_set.add(matchup['t2'])

	time.sleep(.05)
	with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + league_id + "/rosters") as url:
		rosters = json.loads(url.read().decode())

	roster_map = {}
	for roster in rosters:
		roster_map[roster['owner_id']] = roster['roster_id']

	made_playoffs = roster_map[user] in playoff_team_set
	playoff_teams = len(playoff_team_set)

	return playoff_teams, made_playoffs

def buildTable(pick_dict, settings, league_id):
	"""
	"""
	pick_table = pd.DataFrame(columns=['user_id', 'league_id', 'round_1', 'round_2', 'round_3', 'round_4', 'round_5', 'round_6', 
			'round_7', 'round_8', 'round_9', 'round_10', 'round_11', 'round_12', 'scoring_type', 'roster_qb', 'roster_rb', 
			'roster_wr', 'roster_te', 'roster_flex', 'total_teams', 'playoff_teams', 'made_playoffs'])

	for user in pick_dict:
		pick_table = pick_table.append({'user_id': user, 'league_id': league_id, 'round_1': pick_dict[user][1], 'round_2': pick_dict[user][2], 
			'round_3': pick_dict[user][3], 'round_4': pick_dict[user][4], 'round_5': pick_dict[user][5], 'round_6': pick_dict[user][6], 
			'round_7': pick_dict[user][7], 'round_8': pick_dict[user][8], 'round_9': pick_dict[user][9], 'round_10': pick_dict[user][10], 
			'round_11': pick_dict[user][11], 'round_12': pick_dict[user][12], 'scoring_type': settings['scoring_type'], 
			'roster_qb': settings['slots_qb'], 'roster_rb': settings['slots_rb'], 'roster_wr': settings['slots_wr'], 
			'roster_te': settings['slots_te'], 'roster_flex': settings['slots_flex'], 'total_teams': settings['teams'], 
			'playoff_teams': getPlayoffs(user, league_id)[0], 'made_playoffs': getPlayoffs(user, league_id)[1]}, ignore_index=True)

	return pick_table


drafts = pd.DataFrame(columns=['user_id', 'league_id', 'round_1', 'round_2', 'round_3', 'round_4', 'round_5', 'round_6', 
			'round_7', 'round_8', 'round_9', 'round_10', 'round_11', 'round_12', 'scoring_type', 'roster_qb', 'roster_rb', 
			'roster_wr', 'roster_te', 'roster_flex', 'total_teams', 'playoff_teams', 'made_playoffs'])

for league in league_list:
	print(league)
	try:
		draft = getDraft(league)
		picks, settings = getDraft(league)
		if (settings['rounds'] >= 12) & ('slots_qb' in settings) & ('slots_rb' in settings) & ('slots_wr' in settings) & ('slots_flex' in settings) & ('slots_te' in settings):
			print("Passed Test 1")
			pick_dict = buildPickDict(picks)
			print(pick_dict.keys())
			
			all_rounds_present = True
			for user in pick_dict:
				for round in [1,2,3,4,5,6,7,8,9,10,11,12]:
					if round not in pick_dict[user].keys():
						all_rounds_present = False
			if all_rounds_present:
				print("Passed Test 2")
				df = buildTable(pick_dict, settings, league)
				drafts = drafts.append(df, ignore_index=True)
	except:
		print("Error")

drafts.to_csv('fantasy_football_dataset.csv')



# picks, settings = getDraft("597593297883566080")
# pick_dict = buildPickDict(picks)
# print(pick_dict)
# df = buildTable(pick_dict, settings, "597593297883566080")
# print(df)










