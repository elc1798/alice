import fbchat
import getpass

import os, sys, threading
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))
import commands as COMMANDS

class FBListenerBot(fbchat.Client):
    def __init__(self,email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        self.knownfriends = { friend.uid : friend.name for friend in self.getAllUsers() }

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)

        if str(author_id) != str(self.uid):
            feedback = "%s said: %s" % (self.knownfriends[author_id], message)
            os.system(COMMANDS.DISPLAY_NOTIFICATION % (feedback,))

bot = FBListenerBot(str(raw_input("Username: ")), str(getpass.getpass()), debug=False)
t = threading.Thread(target=bot.listen)
t.daemon = True
t.start()

