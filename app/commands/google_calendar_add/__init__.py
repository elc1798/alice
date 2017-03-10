import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))
from utils import google as goog
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

def google_calendar_add_event(query, controller):
    s = query.split(' ')

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

    goog.add_event(" ".join(s))

TRIGGER_MODEL = "GOOGLE_CALENDAR_ADD_EVENT.model"
FUNC = google_calendar_add_event

