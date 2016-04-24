import dota2api
from collections import Counter

# Note, you have to export your Steam Web API key before running this script.
# Like this:
# export D2_API_KEY=yourkeyvaluehere
api = dota2api.Initialise()

# Get hero-id to name map
herolist = api.get_heroes()['heroes']

# one of our matches
# Note this is used to get a simulation of a live game set of players and opponents
# in real use the player ids would be fed from the live match
turnaroundmatch = api.get_match_details(match_id=2314980515)
players = turnaroundmatch['players']

# Find account IDs of all players
accIDs = [p['account_id'] for p in players]
radiant_players = accIDs[0:5]
dire_players = accIDs[5:10]

print('Printing top 5 heroes:')
print('')

for player_set in [radiant_players, dire_players]:
	for player_id in player_set:

		try:
			# most recent 100 matches
			match_his_res = api.get_match_history(account_id=player_id)
		except dota2api.src.exceptions.APIError:
			print('Account ID {} does not allow sniping!'.format(player_id))
			print('')
			continue
		
		matches = match_his_res['matches']

		hero_ids = [next( p['hero_id'] for p in match['players'] if p['account_id'] == player_id ) for match in matches]
		hero_count = Counter(hero_ids).items()
		hero_count = sorted(hero_count, key=lambda x:x[1]) #sort by count

		# replace hero_id by real name
		hero_count = [( next(h['localized_name'] for h in herolist if h['id'] == it[0]), it[1]) for it in hero_count]

		print('Stats for {}'.format(player_id))
		for h in hero_count[-5:]:
			print('{} : {}'.format('#'*h[1], h[0]))
		print('')
