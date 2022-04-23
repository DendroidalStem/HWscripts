from pathlib import Path
from os.path import join

# Chrome cookies location - MUST REPLACE WITH A PROPER PATH!!!
CHROME_COOKIES_PATH = r"C:/Users/luisa/AppData/Local/Google/Chrome/User Data"

# Chrome driver location
DRIVER_PATH = join(str(Path(__file__).parent), "Drivers")
