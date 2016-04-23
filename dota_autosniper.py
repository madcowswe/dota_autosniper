import dota2api
from collections import Counter

# Note, you have to export your Steam Web API key before running this script.
# Like this:
# export D2_API_KEY=yourkeyvaluehere
api = dota2api.Initialise()

# Get hero-id to name map
herolist = api.get_heroes()['heroes']

# one of our matches
turnaroundmatch = api.get_match_details(match_id=2315134143)
players = turnaroundmatch['players']

# find josh in the most obvious way...
JelsdonID = next( p['account_id'] for p in players if p['hero_name'] == 'Dazzle')

# most recent 100 matches
match_his_res = api.get_match_history(account_id=JelsdonID)
matches = match_his_res['matches']

hero_ids = [next( p['hero_id'] for p in match['players'] if p['account_id'] == JelsdonID ) for match in matches]
hero_count = Counter(hero_ids).items()
hero_count = sorted(hero_count, key=lambda x:x[1]) #sort by count

# replace hero_id by real name
hero_count = [( next(h['localized_name'] for h in herolist if h['id'] == it[0]), it[1]) for it in hero_count]

for h in hero_count:
	print('{} : {}'.format('#'*h[1], h[0]))