KILL_ACTIVE_WINDOW = "xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2` > /dev/null 2>&1"
SHUTDOWN = "gnome-session-quit --power-off --no-prompt"
LOCK = "gnome-screensaver-command -l"
SAY = "spd-say -t child_female -p +50 -r -10 \"%s\""
OPEN_FILE_BROWSER = "nautilus ~ &"
VOLUME_CONTROL = "amixer -D pulse sset Master %d%%%s > /dev/null 2>&1"

