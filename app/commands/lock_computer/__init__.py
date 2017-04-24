import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

LOCK = "gnome-screensaver-command -l"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    LOCK = "pmset displaysleepnow"

TRIGGER_MODEL = "LOCK_COMPUTER.model"
FUNC = lambda query, **kwargs: os.system(LOCK)
