import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

KILL_ACTIVE_WINDOW = "xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2` > /dev/null 2>&1"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    KILL_ACTIVE_WINDOW = "FILL THIS IN"

TRIGGER_MODEL = "KILL_ACTIVE_WINDOW.model"
FUNC = lambda query, **kwargs: os.system(KILL_ACTIVE_WINDOW)
