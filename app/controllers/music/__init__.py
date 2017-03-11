import pickle
import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

MODEL_LOCATION = os.path.join(
    CURRENT_DIR,
    "../../../training/models/ordinal_scalers/MUSIC.model"
)

MUSIC_PLAY = "rhythmbox-client --play"
MUSIC_PAUSE = "rhythmbox-client --pause"
MUSIC_NEXT_SONG = "rhythmbox-client --next"
MUSIC_LAST_SONG = "rhythmbox-client --previous"

if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    MUSIC_PLAY = "osascript -e 'tell application \"Spotify\" to play'"
    MUSIC_PAUSE = "osascript -e 'tell application \"Spotify\" to pause'"
    MUSIC_NEXT_SONG = "osascript -e 'tell application \"Spotify\" to next track'"
    MUSIC_LAST_SONG = """
        osascript -e '
        tell application "Spotify"
            set player position to 0
            previous track
        end tell';
        """

class MusicController:

    def __init__(self):
        with open(MODEL_LOCATION, 'r') as m_file:
            self.model = pickle.load(m_file)

    def perform_action(self, sentence):
        myid = self.model.rate(sentence)

        if myid == 0:
            os.system(MUSIC_PLAY)
        elif myid == 1:
            os.system(MUSIC_PAUSE)
        elif myid == 2:
            os.system(MUSIC_NEXT_SONG)
        elif myid == 3:
            os.system(MUSIC_LAST_SONG)

SINGLETON_INSTANCE = MusicController()

# Required method and variable for controllers
def get_instance():
    return SINGLETON_INSTANCE

NAME = "music controller"

