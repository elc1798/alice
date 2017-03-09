import sys

MAC_OS_X_IDENTIFIER = "darwin"
LINUX_IDENTIFIER = "linux"
DISPLAY_NOTIFICATION = "notify-send --urgency=critical --expire-time=5000 --icon=\"face-angel\" \"Alice - Digital Assistant\" \"%s\""

if sys.platform.startswith(MAC_OS_X_IDENTIFIER):
    DISPLAY_NOTIFICATION = "osascript -e 'display notification \"%s\" with title \"Alice - Digital Assistant\"'"
