import fbchat
import getpass

import os, sys, threading
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

class FBListenerBot(fbchat.Client):
    def __init__(self,email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        self.knownfriends = { friend.uid : friend.name for friend in self.getAllUsers() }

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)

        if str(author_id) != str(self.uid):
            feedback = "%s said: %s" % (self.knownfriends[author_id], message)
            os.system(constants.DISPLAY_NOTIFICATION % (feedback,))

GLOBAL_THREAD = None

def start():
    global GLOBAL_THREAD
    if GLOBAL_THREAD is not None:
        return

    bot = FBListenerBot(str(raw_input("Username: ")), str(getpass.getpass()), debug=False)
    GLOBAL_THREAD = threading.Thread(target=bot.listen)
    GLOBAL_THREAD.daemon = True
    GLOBAL_THREAD.start()

def stop():
    pass

