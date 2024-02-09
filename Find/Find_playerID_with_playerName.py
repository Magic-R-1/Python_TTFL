from nba_api.stats.static  import players
player_dict = players.get_players()

#Use ternary operator or write function
#Names are case sensitive
name = 'Donte DiVincenzo'
player =[player for player in player_dict if player['full_name']==name][0]
player_id = player['id']
print(player_id)