KILL_ACTIVE_WINDOW = "xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2` > /dev/null 2>&1"
SHUTDOWN = "gnome-session-quit --power-off --no-prompt"
LOCK = "gnome-screensaver-command -l"
SAY = "spd-say -w -t child_female -p +50 \"%s\""
OPEN_FILE_BROWSER = "nautilus ~ &"
VOLUME_CONTROL = "amixer -D pulse sset Master %d%%%s > /dev/null 2>&1"
VOLUME_GET = "amixer -D pulse get Master"
OPEN_WEB_BROWSER = "sensible-browser \"%s\" 2>&1 /dev/null &"
DISPLAY_NOTIFICATION = "notify-send --urgency=critical --expire-time=5000 --icon=\"face-angel\" \"Alice - Digital Assistant\" \"%s\""
SPOTIFY_PLAY = "rhythmbox-client --play"
SPOTIFY_PAUSE = "rhythmbox-client --pause"
SPOTIFY_NEXT_SONG = "rhythmbox-client --next"
SPOTIFY_LAST_SONG = "rhythmbox-client --previous"

import sys, os, subprocess

if sys.platform == "darwin":
    SPOTIFY_PLAY = "osascript -e 'tell application \"Spotify\" to play'"
    SPOTIFY_PAUSE = "osascript -e 'tell application \"Spotify\" to pause'"
    SPOTIFY_NEXT_SONG = "osascript -e 'tell application \"Spotify\" to next track'"
    SPOTIFY_LAST_SONG = """
                osascript -e '
                tell application "Spotify"
                    set player position to 0
                    previous track
                end tell';
                """
    OPEN_WEB_BROWSER = "open \"%s\" 2>&1 /dev/null &"
    SAY = "xsay -t child_female -p +50 -r -30 \"%s\""
    # The second %s is for compatibility purposes. It will always be
    # substituted with an empty string
    VOLUME_CONTROL = "osascript -e 'set volume  \"%d\"'%s"
    VOLUME_GET = "osascript -e 'get volume settings'"

