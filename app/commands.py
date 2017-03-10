SAY = "spd-say -w -t child_female -p +50 \"%s\""

import sys, os, subprocess

if sys.platform == "darwin":
    SAY = "xsay -t child_female -p +50 -r -30 \"%s\""
    # The second %s is for compatibility purposes. It will always be
    # substituted with an empty string
    NEWS_SAY = "echo \"%s\""
