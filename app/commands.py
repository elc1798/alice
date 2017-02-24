KILL_ACTIVE_WINDOW = "xkill -id `xprop -root _NET_ACTIVE_WINDOW | cut -d\# -f2`"
SHUTDOWN = "gnome-session-quit --power-off --no-prompt"
LOCK = "gnome-screensaver-command -l"
SAY = "spd-say -t child_female -p +69 \"%s\""
OPEN_FILE_BROWSER = "nautilus ~ &"

