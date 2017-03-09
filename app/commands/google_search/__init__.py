import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

GOOGLE_QUERY_URL = "https://www.google.com/search?hl=en&q=%s&btnG=Google+Search&tbs=com&safe=true"
OPEN_WEB_BROWSER = "sensible-browser \"%s\" 2>&1 /dev/null &"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    OPEN_WEB_BROWSER = "open \"%s\" 2>&1 /dev/null &"

remove_list = [ "google", "search", "please", "for" ]
def google_search(query, controllers):
    s = query
    for string in remove_list:
        s = s.replace(string, "", 1)

    s = s.lstrip(' ').replace("'", "\\'").replace("\"", "\\\"")
    site = GOOGLE_QUERY_URL % (s.replace(" ", "+"),)
    os.system(OPEN_WEB_BROWSER % (site,))

TRIGGER_MODEL = "GOOGLE_SEARCH.model"
FUNC = google_search
