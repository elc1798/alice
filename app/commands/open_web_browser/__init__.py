import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

OPEN_WEB_BROWSER = "sensible-browser \"%s\" 2>&1 /dev/null &"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    OPEN_WEB_BROWSER = "open \"%s\" 2>&1 /dev/null &"

def open_web_browser(query, controllers):
    command = query.split(" dot ")
    site = command[0].split(" ")[-1]
    top_level_domain = command[-1]
    if top_level_domain is None:
    #if top_level_domain is not None or not top_level_domain:
        top_level_domain = "com"
    second_level_domain = site + "." + top_level_domain
    os.system(OPEN_WEB_BROWSER % (second_level_domain,))

TRIGGER_MODEL = "OPEN_WEB_BROWSER.model"
FUNC = open_web_browser

