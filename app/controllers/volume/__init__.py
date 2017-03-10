import pickle
import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

MODEL_LOCATION = os.path.join(
    CURRENT_DIR,
    "../../../training/models/ordinal_scalers/VOLUME_CONTROL.model"
)
VOLUME_GET_COMMAND = "amixer -D pulse get Master"
VOLUME_CONTROL_COMMAND = "amixer -D pulse sset Master %d%%%s > /dev/null 2>&1"

if sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
    VOLUME_CONTROL_COMMAND = "osascript -e 'set volume  \"%d\"'%s"

class VolumeController:
    def __init__(self):
        with open(MODEL_LOCATION, 'r') as m_file:
            self.model = pickle.load(m_file)
        self.volume_before_mute = self.get_current_volume()

    def get_current_volume(self):
        if sys.platform.startswith(constants.LINUX_IDENTIFIER):
            s = subprocess.check_output(VOLUME_GET_COMMAND.split(" ")).strip().split("\n")
            matches = __import__("re").search(r"\[([A-Za-z0-9_%]+)\]", s[-2])
            return int(matches.group(1)[:-1])
        elif sys.platform.startswith(constants.MAC_OS_X_IDENTIFIER):
            s = subprocess.check_output(["osascript", "-e", 'get volume settings'])
            return int(s.split(", ")[0].split(":")[1]) / 10
        else:
            return -1

    def update_volume(self, sentence):
        """
        Apologies for the... abundance... of magic numbers. num = 10 declares the
        default "delta" for our volume (in linux). The myid values are derived
        from the clusters from the VOLUME_CONTROL ordinal scaler model (0.txt,
        1.txt, etc.)

        0 - Mute
        1 - Decrease
        2 - Increase
        3 - Unmute
        """
        myid = self.model.rate(sentence)
        modifier = ""
        num = 10

        if myid == 0:
            if self.get_current_volume() != 0:
                self.volume_before_mute = self.get_current_volume()
            num = 0
        elif myid == 1:
            modifier = "-"
        elif myid == 2:
            modifier = "+"
        elif myid == 3:
            modifier = ""
            num = self.volume_before_mute

        if sys.platform.startswith(constants.LINUX_IDENTIFIER) and myid != 3:
            modifier = ""
            # Find the current volume and calculates a lower and higher volume
            num = self.get_current_volume()
            # Janky Mac OS: Get volume gives 0-100, but set volume must be
            # between 0 and 10???? wtf Apple?
            num = (num / 10)
            if myid == 0:
                num = 0
            elif myid == 1:
                num -= 1
            elif myid == 2:
                num += 1

        os.system(VOLUME_CONTROL_COMMAND % (num, modifier))

SINGLETON_INSTANCE = VolumeController()

# Required method and variable for controllers
def get_instance():
    return SINGLETON_INSTANCE

NAME = "volume controller"

