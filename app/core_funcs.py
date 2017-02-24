import os, sys
import commands as COMMANDS

def kill_active_window():
    os.system(COMMANDS.SAY % ("Killing active window",))
    os.system(COMMANDS.KILL_ACTIVE_WINDOW)

def shutdown():
    os.system(COMMANDS.SAY % ("Shutting down",))
    os.system(COMMANDS.SHUTDOWN)
    sys.exit()

def open_file_browser():
    os.system(COMMANDS.SAY % ("Opening file browser",))
    os.system(COMMANDS.OPEN_FILE_BROWSER)

