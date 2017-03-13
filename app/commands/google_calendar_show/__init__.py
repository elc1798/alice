import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))
from utils import google as goog
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

def google_calendar_show_events(query, **kwargs):
    s = query.split(' ')

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

    goog.show_events(s)

TRIGGER_MODEL = "GOOGLE_CALENDAR_SHOW_EVENTS.model"
FUNC = google_calendar_show_events

