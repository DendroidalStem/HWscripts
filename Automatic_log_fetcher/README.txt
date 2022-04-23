Functionality:
The script HW_automatic_log_fetcher.py is written to automatically launch Hero Wars on a Chrome browser window,
automatically click around the game to open the screens required for several API calls to occur,
and then store the result of those API calls in the HW_logs.json file.

Requirements:
In addition to having the selenium python package installed,
the user must provide two pieces of information in the HW_automatic_log_fetcher_user_settings file:
1. The simplest is DRIVER_PATH, the path to the chromedriver.exe file.
If you copy the file structure on the GitHub repository this will already be correct.
Main possible issue would be if the version number of Chrome in your machine doesn't match the version of the webdriver,
in which case you'd need to download a different chrome.exe file
2. Due to some limitations of selenium (and some of my knowledge),
the script can't quite log into the game automatically with your username and password.
Instead, you'll need to make sure you've logged into the game using Chrome at least once by yourself,
then provide the script with CHROME_COOKIES_PATH, the path to where your chrome cookies are stored,
so selenium can use those when running Chrome.
Typically this this path will look like
"C:/Users/{username}/AppData/Local/Google/Chrome/User Data"

Expected issues:
Since the game is running in Flash and it's hard (if not impossible) for selenium to know when flash buttons have been clicked,
the script is written with hard coded waits between clicks. This means that, when assets take too long to load,
the script won't notice that.
In practice this will mean the script may try to click buttons where none exist.
In my experience, this has no negative consequence beyond some logs not being captured, thus needing to run the script again.
In particular, when logging in at the start, the script currently assumes only a 12 second window for the initial loading.
