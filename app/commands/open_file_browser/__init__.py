import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

OPEN_FILE_BROWSER = "nautilus ~ &"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    OPEN_FILE_BROWSER = "open ~ %"

TRIGGER_MODEL = "OPEN_FILE_BROWSER.model"
FUNC = lambda query, **kwargs: os.system(OPEN_FILE_BROWSER)
