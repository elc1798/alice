import os, sys
import pickle, glob

import spacy

from utils import model_matcher as mm
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class Commander:

    def __init__(self, config={}, log_func=None):
        self.model_matcher = None
        self.controllers = {}
        self.officers = {}
        self.monitors = []

        self.log_func = log_func
        if log_func is None:
            def default_log(s, tolerance=0):
                print s

            self.log_func = default_log

        self.nlp = spacy.load('en')

        self.load_models()
        self.load_controllers()
        self.load_commands()

        if config["monitors"] == True:
            self.load_monitors()

    def load_models(self):
        command_model_list = glob.glob("../training/models/commands/*.model")
        self.log_func("Found %d command models" % (len(command_model_list),))

        models = []
        for model_name in command_model_list:
            with open(model_name, 'r') as MODEL_FILE:
                self.log_func("\tLoading << %s >> as command matcher" % (model_name,))
                models.append(pickle.load(MODEL_FILE))

            self.log_func("Loaded model: %s" % (models[-1].name,))

        self.model_matcher = mm.ModelMatcher(models, log_func=self.log_func)

    def load_controllers(self):
        sys.path.insert(0, os.path.join(CURRENT_DIR, "controllers"))
        controller_folders = glob.glob("controllers/*")
        for folder in controller_folders:
            name = os.path.basename(folder)
            temp_module = __import__(name)
            self.controllers[temp_module.NAME] = temp_module.get_instance()

    def load_commands(self):
        sys.path.insert(0, os.path.join(CURRENT_DIR, "commands"))
        command_folders = glob.glob("commands/*")
        for folder in command_folders:
            name = os.path.basename(folder)
            temp_module = __import__(name)
            if temp_module.TRIGGER_MODEL not in self.officers:
                self.officers[temp_module.TRIGGER_MODEL] = []

            self.officers[temp_module.TRIGGER_MODEL].append(temp_module.FUNC)

    def load_monitors(self):
        sys.path.insert(0, os.path.join(CURRENT_DIR, "monitors"))
        monitor_folders = glob.glob("monitors/*")
        for folder in monitor_folders:
            name = os.path.basename(folder)
            temp_module = __import__(name)
            self.monitors.append(temp_module)
            self.monitors[-1].start()

    def stop_monitors(self):
        for mon in self.monitors:
            mon.stop()

    def parse_query(self, res):
        parsed = self.nlp(unicode(res))

        # We want to remove all interjections from our query, since they don't
        # mean much

        significant = [ word for word in parsed if word.dep != spacy.symbols.intj ]
        res = " ".join(map(str, significant))

        res = res.replace(".", " dot ").lower()

        self.log_func("Parsed query: '%s'" % (res,), tolerance=1)

        matches = self.model_matcher.get_matches(res)
        for match in matches:
            for officer_action in self.officers[match]:
                officer_action(
                    res,
                    controllers=self.controllers,
                    nlp=self.nlp,
                    log_func=self.log_func
                )

class Dummy(Commander):

    # Override __init__
    def __init__(self, config={}, log_func=None):
        self.model_matcher = None
        self.controllers = {}
        self.officers = {}
        self.monitors = []

        self.log_func = log_func
        if log_func is None:
            def default_log(s, tolerance=0):
                print s

            self.log_func = default_log

        self.load_models()
        self.nlp = spacy.load('en')

    # Override parse_query
    def parse_query(self, res):
        print "This is a test session. Enter '!' to exit"
        if res == "!":
            sys.exit()

        parsed = self.nlp(unicode(res))

        # We want to remove all interjections from our query, since they don't
        # mean much

        significant = [ word for word in parsed if word.dep != spacy.symbols.intj ]
        res = " ".join(map(str, significant))

        res = res.replace(".", " dot ").lower()

        self.log_func("Parsed query: '%s'" % (res,), tolerance=1)

        matches = self.model_matcher.get_matches(res)
        print matches

