import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants
from datetime import datetime

def get_time(query, controllers):
    hour = datetime.now().hour
    minutes = datetime.now().minute
    is_morning = hour < 12
    hour = (hour % 12)
    if hour == 0:
        hour = 12

    curr_time = "%d %02d" % (hour, minutes)
    if is_morning:
        curr_time += " A.M."
    else :
        curr_time += " P.M."

    os.system(constants.DISPLAY_NOTIFICATION % (curr_time,))

TRIGGER_MODEL = "GET_TIME.model"
FUNC = get_time
