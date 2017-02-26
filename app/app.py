import os, sys, subprocess
import pickle
import glob
import argparse
import core_funcs
import fbchat
import getpass

# Version Control Constants
APPLICATION_NAME = "Alice"
APPLICATION_RELEASE = 0
APPLICATION_REVISION = 0

should_listen = False
VERBOSITY = 0

prompts = [ "hey alice", "alice", "okay alice", "hey alex", "alex", "okay alex" ]
alice = None

class AliceReceiver(fbchat.Client):
    def __init__(self,email, password, debug=True, user_agent=None):
        fbchat.Client.__init__(self,email, password, debug, user_agent)
        self.knownfriends = { friend.uid : friend.name for friend in self.getAllUsers() }

    def on_message(self, mid, author_id, author_name, message, metadata):
        self.markAsDelivered(author_id, mid)
        self.markAsRead(author_id)

        if str(author_id) != str(self.uid):
            print message
            parse_query(message)

def log(s, tolerance=1):
    global VERBOSITY

    if VERBOSITY >= tolerance:
        print(s)

def parse_query(res):
    # For open_web_browser
    res = res.replace('.', ' dot ')
    cross_check_models(res)

models = []
volume_controller = None
spotify_controller = None

def load_models():
    global models, volume_controller, spotify_controller
    model_list = glob.glob("../training/MODELS/*.model")
    log("Found %d models" % (len(model_list),))
    for model_name in model_list:
        with open(model_name, 'r') as MODEL_FILE:
            if model_name.endswith("ORDINAL_SCALE_VOLUME_CONTROL.model"):
                log("\tLoading << %s >> as volume controller" % (model_name,))
                volume_controller = core_funcs.VolumeController(pickle.load(MODEL_FILE))
            elif model_name.endswith("ORDINAL_SCALE_SPOTIFY.model"):
                log("\tLoading << %s >> as spotify controller" % (model_name,))
                spotify_controller = core_funcs.SpotifyController(pickle.load(MODEL_FILE))
            else:
                log("\tLoading << %s >> as command matcher" % (model_name,))
                models.append(pickle.load(MODEL_FILE))
        log("Loaded model: %s" % (models[-1].name,))

def cross_check_models(sentence):
    global volume_controller, spotify_controller
    log("Checking << %s >> with existing models..." % (sentence,))

    matched = None
    for model in models:
        if model.match(sentence):
            log("Matched with %s" % (model.name,))
            if matched == None:
                matched = model.name
            else:
                log("Error: MULTIPLE MATCHES")
                return None
        else:
            log("Did not match with %s" % (model.name,), tolerance=2)
    if matched == None:
        return None
    if matched == "SPOTIFY.model":
        spotify_controller.perform_action(sentence)
    elif matched == "VOLUME_CONTROL.model":
        volume_controller.perform_action(sentence)
    else:
        alice.command_mapping[matched](sentence)

def main():
    global use_voice

    if use_voice:
        recognize = AliceReceiver(str(raw_input("Alice login: ")),
                str(getpass.getpass()), debug=False)
        print("Alice is listening on Facebook!")
        recognize.listen()
    else:
        while True:
            query = str(raw_input("alice > "))
            parse_query(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alice - Linux Virtual Assistant")
    parser.add_argument("--use-voice", "-V", action="store_true")
    parser.add_argument("--talk", "-t", action="store_true")
    parser.add_argument("--test", "-T", action="store_true")
    parser.add_argument("--facebook", "-f", action="store_true")
    parser.add_argument("--monitor", "-m", action="store_true")
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--version', action='version', version="%s %d.%d" %
            (APPLICATION_NAME, APPLICATION_RELEASE, APPLICATION_REVISION))

    args = parser.parse_args()

    use_voice = args.use_voice
    VERBOSITY = args.verbose
    load_models()
    if args.test:
        alice = core_funcs.DummyActuator()
    else:
        alice = core_funcs.CommandActuator(
                    talk=args.talk,
                    volume_controller=volume_controller
                )

    if args.facebook:
        from services import facebook

    if args.monitor:
        from services import system_monitor

    from services import package_checker
    main()

