import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

import requests

HTTP_ERROR_CODE_START = 400
HTTP_ERROR_MESSAGE_FORMAT= "Site '%s' returned error '%d'"
REQUEST_ERROR_FORMAT = "Requesting connection to '%s' errored!"
HYPERTEXT_FORMAT_CODES = [ "http://", "https://" ]

OPEN_WEB_BROWSER = "sensible-browser \"%s\" 2>&1 /dev/null &"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    OPEN_WEB_BROWSER = "open \"%s\" 2>&1 /dev/null &"

SYS_CMD = lambda x : os.system(OPEN_WEB_BROWSER % (x,))

def open_web_browser(query, **kwargs):
    sites = []

    parsed = kwargs["nlp"](unicode(query.replace(" dot ", ".")))
    for token in parsed:
        if token.like_url:
            sites.append(str(token.text))

    kwargs["log_func"]( sites, tolerance=2 )
    for site in sites:
        for hypertext_code in HYPERTEXT_FORMAT_CODES:
            try:
                url = "%s%s" % (hypertext_code, site)
                response = requests.get(url)
            except:
                kwargs["log_func"](REQUEST_ERROR_FORMAT % (site,), tolerance=1)
                continue

            if response.status_code < HTTP_ERROR_CODE_START:
                SYS_CMD(site)
                break
            else:
                error_msg = HTTP_ERROR_MESSAGE_FORMAT % (site, response.status_code)
                kwargs["log_func"](error_msg, tolerance=1)

TRIGGER_MODEL = "OPEN_WEB_BROWSER.model"
FUNC = open_web_browser

