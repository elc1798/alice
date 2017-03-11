import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

def update_music(query, controllers):
    controllers["music controller"].perform_action(query)

TRIGGER_MODEL = "MUSIC.model"
FUNC = update_music
