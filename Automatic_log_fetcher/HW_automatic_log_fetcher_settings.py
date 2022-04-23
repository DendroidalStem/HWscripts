from pathlib import Path
from os.path import join

# HW url

URL = r"https://www.hero-wars.com"
API_URL = r'https://heroes-wb.nextersglobal.com/api/'

# Log file location path
LOG_FILE_PATH = join(str(Path(__file__).parent), "HW_logs.json")

# Button locations

BUTTON_LOGIN_OFFER_CLOSE = (468, -222)
BUTTON_SEASON_OFFER_CLOSE = (390, -255)

BUTTON_ARENA = (100, -30)
BUTTON_ARENA_LOG = (200, -190)
BUTTON_ARENA_LOG_CLOSE = (355, -210)
BUTTON_ARENA_CLOSE = (412, -243)

BUTTON_GA = (215, -160)
BUTTON_GA_LOG = (215, -175)
BUTTON_GA_LOG_CLOSE = (355, -230)
BUTTON_GA_CLOSE = (430, -228)

BUTTON_CITY_GUILD_SWITCH = (-440, 235)

BUTTON_ASCENSION = (-305, 145)
BUTTON_GUILD_RAID = (-370, -60)
BUTTON_GUILD_RAID_LOG = (400, 255)
BUTTON_GUILD_RAID_SET_LEVEL = (-405, -282)
BUTTON_GUILD_SCREEN_CLOSE = (460, -282)

BUTTON_GUILD_WAR = (255, -115)
