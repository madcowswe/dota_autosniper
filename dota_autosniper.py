import dota2api
from collections import Counter
from time import sleep


# Note, you have to export your Steam Web API key before running this script.
# Like this:
# export D2_API_KEY=yourkeyvaluehere
api = dota2api.Initialise()

# Get hero-id to name map
herolist = api.get_heroes()['heroes']


def snipe_player(player_id):
	player_id = int(player_id)
	try:
		# most recent 100 matches
		match_his_res = api.get_match_history(account_id=player_id)
	except dota2api.src.exceptions.APIError:
		print('Account ID {} does not allow sniping!'.format(player_id))
		print('')
		return
	
	matches = match_his_res['matches']

	hero_ids = [next( p['hero_id'] for p in match['players'] if p['account_id'] == player_id ) for match in matches]
	hero_count = Counter(hero_ids).items()
	hero_count = sorted(hero_count, key=lambda x:x[1]) #sort by count

	# replace hero_id by real name
	hero_count = [( next(h['localized_name'] for h in herolist if h['id'] == it[0]), it[1]) for it in hero_count]

	print('Stats for {}'.format(player_id))
	for h in hero_count[-10:]:
		print('{} : {}'.format('#'*h[1], h[0]))
	print('')

def dump_playerstats_from_match(match_id):
	thematch = api.get_match_details(match_id=match_id)
	players = thematch['players']

	# Find account IDs of all players
	accIDs = [p['account_id'] for p in players]
	radiant_players = accIDs[0:5]
	dire_players = accIDs[5:10]

	print('Printing top 10 heroes:')
	print('')

	for player_set in [radiant_players, dire_players]:
		for player_ida in player_set:
			snipe_player(player_ida)


# dump_playerstats_from_match(2328943922)

# Scan clipboard for changes
# This only works on Cygwin. TODO: implement for other platforms
with open('/dev/clipboard', 'r') as f:
	clipstate = f.read()

while True:
	with open('/dev/clipboard', 'r') as f:
		new_clip = f.read()
		if new_clip and new_clip != clipstate:
			clipstate = new_clip
			snipe_player(clipstate)
	sleep(0.2)
