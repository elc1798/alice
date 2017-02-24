import os, sys
import commands as COMMANDS


class CommandActuator:

    def __init__(self, talk=True):
        self.command_mapping = {
            "EXIT_ALICE.model" : self.exit,
            "KILL_ACTIVE_WINDOW.model" : self.kill_active_window,
            "SHUTDOWN_COMPUTER.model" : self.shutdown,
            "VOLUME_CONTROL.model" : self.volume,
            "LOCK_COMPUTER.model" : self.lock
        }
        self.talk = talk

    def exit(self, s):
        sys.exit()

    def kill_active_window(self, s):
        if self.talk:
            os.system(COMMANDS.SAY % ("Killing active window",))
        os.system(COMMANDS.KILL_ACTIVE_WINDOW)

    def shutdown(self, s):
        if self.talk:
            os.system(COMMANDS.SAY % ("Shutting down",))
        os.system(COMMANDS.SHUTDOWN)
        sys.exit()

    def open_file_browser(self, s):
        if self.talk:
            os.system(COMMANDS.SAY % ("Opening file browser",))
        os.system(COMMANDS.OPEN_FILE_BROWSER)

    def volume(self, s):
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

    def lock(self, s):
        os.system(COMMANDS.LOCK)

class DummyActuator:
    def __init__(self, talk=True):
        self.command_mapping = {
            "EXIT_ALICE.model" : sys.exit,
            "KILL_ACTIVE_WINDOW.model" : self.no_op,
            "SHUTDOWN_COMPUTER.model" : self.no_op,
            "VOLUME_CONTROL.model" : self.no_op,
            "LOCK_COMPUTER.model" : self.no_op
        }

    def no_op(self, s):
        pass

