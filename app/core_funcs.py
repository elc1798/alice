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

    def __init__(self, talk=True, volume_controller=None):
        self.command_mapping = {
            "GOOGLE_CALENDAR_SHOW_EVENTS.model" : self.google_calendar_show_events,
            "GOOGLE_CALENDAR_ADD_EVENT.model" : self.google_calendar_add_event,
            "GOOGLE_MAIL_LIST_MAIL.model" : self.google_mail_list_mail,
        }
        self.talk = talk
        self.volume_controller = volume_controller

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

