import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

SHUTDOWN = "gnome-session-quit --power-off --no-prompt"
if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    SHUTDOWN = "osascript -e 'tell app \"System Events\" to shut down'"

def shutdown(query, **kwargs):
    os.system(SHUTDOWN)
    sys.exit()

TRIGGER_MODEL = "SHUTDOWN.model"
FUNC = shutdown
