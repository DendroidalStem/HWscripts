import os
import json

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from time import sleep

from HW_automatic_log_fetcher_settings import *
from HW_automatic_log_fetcher_user_settings import *

########################################
# Setting up chrome driver

os.environ['PATH'] += ';' + DRIVER_PATH   # allows python to find chromedriver

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(
    'user-data-dir=' + CHROME_COOKIES_PATH)
# chrome_options.add_argument("--auto-open-devtools-for-tabs")

capabs = DesiredCapabilities.CHROME
capabs['goog:loggingPrefs'] = {'performance': 'ALL'}

########################################


def main(log_types):

    with webdriver.Chrome(options=chrome_options, desired_capabilities=capabs) as driver:
        # loading game
        driver.get(URL)
        sleep(12)

        ################################
        # Visiting required game screens

        game_screen = driver.find_element(By.ID, "flash-content")
        actions = ActionChains(driver)

        def click_button(button_location, wait_time):
            actions.move_to_element(game_screen)
            actions.move_by_offset(*button_location)
            actions.click()
            actions.pause(wait_time)

        click_button(BUTTON_LOGIN_OFFER_CLOSE, .5)
        click_button(BUTTON_SEASON_OFFER_CLOSE, .5)

        # for pos in [BUTTON_ARENA, BUTTON_ARENA_LOG, BUTTON_ARENA_LOG_CLOSE, BUTTON_ARENA_CLOSE]:
        #     click_button(pos, .5)
        #
        # for pos in [BUTTON_GA, BUTTON_GA_LOG, BUTTON_GA_LOG_CLOSE, BUTTON_GA_CLOSE]:
        #     click_button(pos, .5)

        click_button(BUTTON_CITY_GUILD_SWITCH, 5)

        click_button(BUTTON_ASCENSION, 5)
        click_button(BUTTON_GUILD_RAID, 1)
        click_button(BUTTON_GUILD_RAID_SET_LEVEL, 5)
        click_button(BUTTON_GUILD_SCREEN_CLOSE, .5)
        click_button(BUTTON_GUILD_RAID_LOG, 2.5)
        click_button(BUTTON_GUILD_SCREEN_CLOSE, .5)
        click_button(BUTTON_GUILD_SCREEN_CLOSE, .5)
        click_button(BUTTON_GUILD_SCREEN_CLOSE, .5)

        click_button(BUTTON_GUILD_WAR, 3)
        click_button(BUTTON_GUILD_SCREEN_CLOSE, .5)

        actions.perform()

        ################################
        # processing API calls

        with open(LOG_FILE_PATH) as f:
            local_log_json = json.load(f)

        logs_raw = driver.get_log('performance')
        logs = [json.loads(log["message"])['message'] for log in logs_raw]
        logs = [log for log in logs if log['method'] == 'Network.responseReceived']

        missing_log_types = set(log_types)

        for log in logs:
            request_id = log["params"]["requestId"]
            resp_url = log["params"]["response"]["url"]
            if resp_url == API_URL and \
                    log["params"]["response"]["mimeType"] == "application/javascript":
                try:
                    post_data = driver.execute_cdp_cmd(
                        "Network.getRequestPostData", {"requestId": request_id})
                    post_data = post_data['postData']
                    post_data = json.loads(post_data)
                    for i, call in enumerate(post_data['calls']):
                        name = call['name']
                        if name in log_types:
                            response = driver.execute_cdp_cmd(
                                "Network.getResponseBody", {"requestId": request_id})
                            response = response['body']
                            response = json.loads(response)
                            response = response['results'][i]

                            # save response to log file; two cases depending on whether call has arguments
                            if not call['args']:
                                local_log_json[name] = response['result']['response']
                                print(f"Updated {name}")
                            else:
                                type = call['args']['type']
                                if name not in local_log_json:
                                    local_log_json[name] = {}
                                local_log_json[name][type] = response['result']['response']
                                print(f"Updated {name}, {type}")

                            missing_log_types.remove(name)

                except:
                    print('badada')

        print('')
        if not missing_log_types:
            print('All log types found')
        else:
            for type in missing_log_types:
                print(f'Missing log:{type}')

        with open(LOG_FILE_PATH, 'w') as f:
            json.dump(local_log_json, f, indent=4)

        ################################

        sleep(5)

#############


if __name__ == '__main__':
    main(['clanGetInfo',
          'clanRaid_logStats', 'clanRaid_logBoss',
          'clanWarGetDefence', 'inventoryGet',
          # 'battleGetByType',
          'clanRaid_getInfo', 'clanRaid_getDifficulty'])
