import json
import os
from collections import defaultdict
from pathlib import Path

from process_member_data import find_member_order, find_member_names
from spreadsheet_conversion import create_spreadsheet

directory = str(Path(__file__).parent)

# member data from dependencies
current_user_order = find_member_order()
user_id_to_name = find_member_names()


# Asgard log
filename = 'clanRaid_logStats&Nodes&Boss.json'

with open(os.path.join(directory, filename)) as f:
    NodesBossLog = json.load(f)

data = NodesBossLog['results']


def main():
    header_row = [
        {'value': "Player/Teams", 'color_type': 'UIcorner'},
        {'value': "team1", 'color_type': 'UI'},
        {'value': "team2", 'color_type': 'UI'},
        {'value': "team3", 'color_type': 'UI'},
        {'value': "team4", 'color_type': 'UI'},
        {'value': "team5", 'color_type': 'UI'},
        {'value': "Morale points", 'color_type': "UI"}
    ]

    #######################################

    logStats = data[-3]['result']['response']
    logBoss = data[-1]['result']['response']

    #######################################
    # create dictonary with ordered list boss attacks per member

    table_dict = defaultdict(list)
    for user in current_user_order:
        if user in logBoss:
            battles = logBoss[user]
            for timestamp in sorted(battles.keys()):
                battle = battles[timestamp]
                damage_done = sum(battle['result']['damage'].values())
                # if sum(1 for damage in battle['result']['damage'].values() if damage) > 1:
                # this identifies fights where boss level changes
                # print('banana')
                level = battle['result']['level']
                table_dict[user].append({'value': damage_done, 'color_type': level})
        else:
            table_dict[user] = []

    # add empty entries to lists (for missing attacks) and append morale points to lists

    for user, meh in logStats.items():
        table_dict[user] += [{'value': 0, 'color_type': '0'}]*(5-len(table_dict[user]))
        table_dict[user].append({'value': meh["nodesPoints"], 'color_type': '1'})

    # convert number ids to user names

    table_dict = {user_id_to_name[k]: v for k, v in table_dict.items()}

    # convert dict to a table/matrix, add column for user names and header row

    table = [[{'value': k, 'color_type': 'UI'}] + v for k, v in table_dict.items()]
    table = [header_row] + table

    ############
    # Save table as a spreadsheet
    create_spreadsheet(table, "TeamGuildRaidLog.xlsx")


if __name__ == '__main__':
    main()
