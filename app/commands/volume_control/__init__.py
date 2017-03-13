import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

def update_volume(query, **kwargs):
    kwargs["controllers"]["volume controller"].update_volume(query)

TRIGGER_MODEL = "VOLUME_CONTROL.model"
FUNC = update_volume
