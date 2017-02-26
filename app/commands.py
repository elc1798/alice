KILL_ACTIVE_WINDOW = "xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2` > /dev/null 2>&1"
SHUTDOWN = "gnome-session-quit --power-off --no-prompt"
LOCK = "gnome-screensaver-command -l"
SAY = "spd-say -t child_female -p +50 -r -30 \"%s\""
OPEN_FILE_BROWSER = "nautilus ~ &"
VOLUME_CONTROL = "amixer -D pulse sset Master %d%%%s > /dev/null 2>&1"
OPEN_WEB_BROWSER = "sensible-browser \"%s\" 2>&1 /dev/null &"
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
