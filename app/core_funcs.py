import os, sys
import urllib
import commands as COMMANDS
from datetime import datetime
from services import google as goog
import subprocess

class CommandActuator:

    GOOGLE_QUERY_URL = "https://www.google.com/search?hl=en&q=%s&btnG=Google+Search&tbs=com&safe=true"

    def __init__(self, talk=True, volume_controller=None):
        self.command_mapping = {
            "EXIT_ALICE.model" : self.exit,
            "KILL_ACTIVE_WINDOW.model" : self.kill_active_window,
            "SHUTDOWN_COMPUTER.model" : self.shutdown,
            "VOLUME_CONTROL.model" : self.volume,
            "LOCK_COMPUTER.model" : self.lock,
            "OPEN_WEB_BROWSER.model" : self.open_web_browser,
            "GOOGLE_SEARCH.model" : self.google_search,
            "GOOGLE_CALENDAR_SHOW_EVENTS.model" : self.google_calendar_show_events,
            "GET_TIME.model" : self.get_time
        }
        self.talk = talk
        self.volume_controller = volume_controller

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
        if self.volume_controller == None:
            intersect = lambda l1, l2 : [ i for i in l1 if i in l2 ]
            t = (0, "")
            if "mute" in s:
                t = (0, "")
            elif len(intersect(["higher","louder","increase","up"], s.split(" "))) > 0:
                t = (5, "+")
            elif len(intersect(["lower","softer","quieter","decrease","down"],s.split(" "))) > 0:
                t = (5, "-")
            os.system(COMMANDS.VOLUME_CONTROL % t)
        else:
            self.volume_controller.adjust(s)

    def lock(self, s):
        os.system(COMMANDS.LOCK)

    def open_web_browser(self, s):
        command = s.split(" dot ")
        site = command[0].split(" ")[-1]
        top_level_domain = command[-1]
        if top_level_domain is not None or not top_level_domain:
            top_level_domain = "com"
        second_level_domain = site + "." + top_level_domain
        os.system(COMMANDS.OPEN_WEB_BROWSER % (second_level_domain,))

    def google_search(self, s):
        if (s.count("google") >= 1):
            s = s.replace("google", "", 1)
        if (s.count("search") >= 1):
            s = s.replace("search", "", 1)
        if (s.count("please") >= 1):
            s = s.replace("please", "", 1)
        if (s.count("for") >= 1):
            s = s.replace("for", "", 1)
        s = s.lstrip(' ').replace("'", "\\'").replace("\"", "\\\"")
        site = CommandActuator.GOOGLE_QUERY_URL % (s.replace(" ", "+"),)
        os.system(COMMANDS.OPEN_WEB_BROWSER % (site,))

    def google_calendar_show_events(self, s):
        s = s.split(' ')
        date = 'today'

        if 'on' in s:
            index = s.index('on') + 1
            s = s[index:]
        elif 'for' in s:
            index = s.index('for') + 1
            s = s[index:]
        elif 'in' in s:
            index = s.index('in') + 1
            s = s[index:]
        elif 'to do' in s:
            index = s.index('to do') + 1
            s = s[index:]
        else:
            s = 'today'

        goog.ShowEvents(s)

    def get_time(self, s):
        hour = datetime.now().hour
        minutes = datetime.now().minute
        is_morning = hour < 12
        hour = (hour % 12)
        if hour == 0:
            hour = 12

        curr_time = "%d %d" % (hour, minutes)
        if is_morning:
            curr_time += "A.M."
        else :
            curr_time += "P.M."

        os.system(COMMANDS.DISPLAY_NOTIFICATION % (curr_time,))
        os.system(COMMANDS.SAY % (curr_time,))

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

class SpotifyController:

    def __init__(self, spotify_ordinal_scale_model):
        print("init")
        self.model = spotify_ordinal_scale_model

    def perform_action(self, sentence):
        myid = self.model.rate(sentence)

        if (myid == 0 and COMMANDS.SPOTIFY_PLAY!= None):
            os.system(COMMANDS.SPOTIFY_PLAY)
        elif (myid == 1 and COMMANDS.SPOTIFY_PAUSE!= None):
            os.system(COMMANDS.SPOTIFY_PAUSE)
        elif (myid == 2 and COMMANDS.SPOTIFY_NEXT_SONG!= None):
            os.system(COMMANDS.SPOTIFY_NEXT_SONG)
        elif (myid == 3 and COMMANDS.SPOTIFY_LAST_SONG!= None):
            os.system(COMMANDS.SPOTIFY_LAST_SONG)

class VolumeController:

    def __init__(self, volume_ordinal_scale_model):
        self.model = volume_ordinal_scale_model

    def perform_action(self, sentence):
        myid = self.model.rate(sentence)
        modifier = ""
        num = 0 if myid == 0 else 5

        if myid == 1:
            modifier = "-"
        elif myid == 2:
            modifier = "+"

        if sys.platform == "darwin":
            modifier = ""
            # Find the current volume and calculates a lower and higher volume
            current_volume  = "osascript -e 'get volume settings' | cut -d':' -f2 | cut -d',' -f1"
            s = subprocess.check_output(["osascript", "-e", 'get volume settings'])
            num = int(s.split(", ")[0].split(":")[1])
            # Janky Mac OS: Get volume gives 0-100, but set volume must be
            # between 0 and 10???? wtf Apple?
            num = (num / 10)
            if myid == 0:
                num = 0
            elif myid == 1:
                num -= 1
            elif myid == 2:
                num += 1

        os.system(COMMANDS.VOLUME_CONTROL % (num, modifier))



