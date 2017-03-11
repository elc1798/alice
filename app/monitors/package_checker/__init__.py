import subprocess
import os, sys, threading, time
from datetime import datetime

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

APT_GET_UPDATES = "apt-get upgrade -s"
PIP_UPDATES = "pip list -o"
OUTDATED_NOTIFICATION = "There are %d outdated packages in %s"

should_continue = True

def get_num_apt_upgrades():
    global APT_GET_UPDATES
    apt_update_string = subprocess.check_output(APT_GET_UPDATES.split(" "))
    significant_data = None
    for line in apt_update_string.split("\n"):
        if "newly installed" in line and "to remove" in line:
            significant_data = line
    return int(significant_data.split(" upgraded")[0])

def get_num_pip_upgrades():
    global PIP_UPDATES
    with open(os.devnull, 'w') as devnull:
        pip_update_string = subprocess.check_output(PIP_UPDATES.split(" "), stderr=devnull)
    return len(pip_update_string.strip().split("\n"))

def display_notification(service, num):
    global OUTDATED_NOTIFICATION
    feedback = OUTDATED_NOTIFICATION % (num, service)
    os.system(constants.DISPLAY_NOTIFICATION % (feedback,))

def hourly_check():
    global should_continue

    while should_continue:
        if datetime.now().minute == 0:
            apt_num = get_num_apt_upgrades()
            pip_num = get_num_pip_upgrades()
            if apt_num > 0:
                display_notification("Apt", apt_num)
            if pip_num > 0:
                display_notification("Pip", pip_num)
        time.sleep(60)

GLOBAL_THREAD = None

def start():
    global GLOBAL_THREAD
    if GLOBAL_THREAD is not None:
        return

    GLOBAL_THREAD = threading.Thread(target=hourly_check)
    GLOBAL_THREAD.daemon = True
    GLOBAL_THREAD.start()

def stop():
    global should_continue

    should_continue = False

if __name__ == "__main__":
    print get_num_apt_upgrades()
    print get_num_pip_upgrades()

