import fbchat

class AliceReceiver(fbchat.Client):
    def __init__(self, email, password, callback, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        self.knownfriends = { friend.uid : friend.name for friend in self.getAllUsers() }
        self.callback = callback

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)
        self.markAsRead(author_id)

        if str(author_id) != str(self.uid) and str(author_id) in self.knownfriends:
            self.callback(message)

