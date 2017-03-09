import os, sys
import urllib
import commands as COMMANDS
from datetime import datetime
from services import google as goog
import subprocess
import urllib2
import json
import pyowm

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
            "GOOGLE_CALENDAR_ADD_EVENT.model" : self.google_calendar_add_event,
            "GOOGLE_MAIL_LIST_MAIL.model" : self.google_mail_list_mail,
            "GET_TIME.model" : self.get_time,
            "GET_NEWS.model" : self.get_news, 
            "GET_WEATHER.model" : self.get_weather
        }
        self.talk = talk
        self.volume_controller = volume_controller

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
        if top_level_domain is None:
        #if top_level_domain is not None or not top_level_domain:
            top_level_domain = "com"
        second_level_domain = site + "." + top_level_domain
        os.system(COMMANDS.OPEN_WEB_BROWSER % (second_level_domain,))

    def google_calendar_show_events(self, s):
        s = s.split(' ')

        if 'on' in s:
            index = s.index('on') + 1
            s = s[index:]
        elif 'for' in s:
            index = s.index('for') + 1
            s = s[index:]
        elif 'in' in s:
            index = s.index('in') + 1
            s = s[index:]
        elif ' to do ' in s:
            index = s.index('to do') + 1
            s = s[index:]
        else:
            s = 'today'

        goog.ShowEvents(s)

    def google_calendar_add_event(self, s):
        s = s.split(' ')

        if "event for" in s:
            index = s.index("event for") + 1
            s = s[index:]
        elif "event on" in s:
            index = s.index("event on") + 1
            s = s[index:]
        elif "event to" in s:
            index = s.index("event to") + 1
            s = s[index:]
        elif "event please" in s:
            index = s.index("event please") + 1
            s = s[index:]
        else: #" event " in s:
            index = s.index("event") + 1
            s = s[index:]

        goog.AddEvent(s)

    def google_mail_list_mail(self, s):
        s = ['UNREAD']
        goog.ListMail(s)


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

