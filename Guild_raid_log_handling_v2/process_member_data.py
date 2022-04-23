# Utilities for ordering guild members by strength (in GW defense)

import json
import os
from pathlib import Path

#########################################
# Paths for the needed API logs
# mainLog is accessed when initiating the game,
# and clanWar log is accessed when checking GW defense

directory = str(Path(__file__).parent)
mainLog_path = os.path.join(directory, r'../Automatic_log_fetcher/HW_logs.json')

###################################
# Opening the logs as dictionaries

# with open(clanWarGetDefense_path) as f:
#     clanWarGetDefense_log = json.load(f)

with open(mainLog_path) as f:
    main_log = json.load(f)

#########################################
# Auxiliary functions for:
# - ordering guild members ID numbers by strength (in GW defense)
# - converting ID numbers to user names


def find_member_order():
    data = main_log['clanWarGetDefence']['teams']

    user_powers = {}
    for user, cat in data.items():
        heroes_power = sum(hero['power'] for hero in cat['clanDefence_heroes']['units'].values())
        titans_power = sum(hero['power'] for hero in cat['clanDefence_titans']['units'].values())
        user_powers[user] = heroes_power + titans_power

    return sorted(user_powers.keys(), key=lambda user: user_powers[user], reverse=True)


def find_member_names():
    member_data = main_log["clanGetInfo"]["clan"]["members"]

    return {k: v['name'] for k, v in member_data.items()}


print(find_member_order())
print(find_member_names())
