import os, sys
import commands as COMMANDS

def exit(s):
    sys.exit()

def kill_active_window(s):
    os.system(COMMANDS.SAY % ("Killing active window",))
    os.system(COMMANDS.KILL_ACTIVE_WINDOW)

def shutdown(s):
    os.system(COMMANDS.SAY % ("Shutting down",))
    os.system(COMMANDS.SHUTDOWN)
    sys.exit()

def open_file_browser(s):
    os.system(COMMANDS.SAY % ("Opening file browser",))
    os.system(COMMANDS.OPEN_FILE_BROWSER)

def volume(s):
    # Statement intensity inference is a planned feature and I am currently
    # working on it. For now, for simplicity's sake, below is a naive
    # implementation on moving the audio up or down

    intersect = lambda l1, l2 : [ i for i in l1 if i in l2 ]
    t = (0, "")
    if "mute" in s:
        t = (0, "")
    elif len(intersect(["higher","louder","increase","up"], s.split(" "))) > 0:
        t = (5, "+")
    elif len(intersect(["lower","softer","quieter","decrease","down"],s.split(" "))) > 0:
        t = (5, "-")
    os.system(COMMANDS.VOLUME_CONTROL % t)

def lock(s):
    os.system(COMMANDS.LOCK)

