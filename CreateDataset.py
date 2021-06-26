
"""
Pseduocode

league_list <- [<init_league>]
checked_league_list <- []
user_list <- []
checked_user_list <- []

while (no change in league list or user list between two consective loops):

	leagues_to_check = league_list - checked_league_list
	for league in leagues_to_check:
		user_list.append(all users in league)
		checked_league_list.append(league)

	users_to_check = user_list - checked_user_list
	for user in users_to_check:
		league_list.append(all leagues for user)
		checked_users.append(users)
"""

import urllib.request
import json

league_set =set(["597593297883566080"])
checked_league_set = set()
user_set = set()
checked_user_set = set()

def getUsers(league_id):
	"""
	Given a league_id, fetch all users in the league
	Return a list of all users
	"""

	#get owners, flatten metadata, and extract user_id, roster_id, and team_name
	with urllib.request.urlopen("https://api.sleeper.app/v1/league/" + league_id + "/users") as url:
	    owners = json.loads(url.read().decode())
	
	user_list = [i['user_id'] for i in owners]
	return(user_list)

def getLeagues(user_id):
	"""
	Given a user_id, fetch all leagues in which the user is a member
	Return a list of all leagues
	"""

	#get users
	with urllib.request.urlopen("https://api.sleeper.app/v1/user/" + user_id + "/leagues/nfl/2020") as url:
	    leagues = json.loads(url.read().decode())
	
	league_list = [i['league_id'] for i in leagues]
	return(league_list)

stopping_condition = True
iteration_counter = 0

while stopping_condition & (iteration_counter < 5):



	leagues_to_check = league_set.difference(checked_league_set)
	for league in leagues_to_check:
		user_set.update(getUsers(league))
		checked_league_set.update(league)

	users_to_check = user_set.difference(checked_user_set)
	for user in users_to_check:
		league_set.update(getLeagues(user))
		checked_user_set.update(user)

	
	iteration_counter += 1


print(league_set)
print(user_set)
 