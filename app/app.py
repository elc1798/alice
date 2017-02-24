import os, sys, subprocess
import pickle
import glob

import speech_recognition as sr
import core_funcs

command_mapping = {
    "EXIT_ALICE.model" : core_funcs.exit,
    "KILL_ACTIVE_WINDOW.model" : core_funcs.kill_active_window,
    "SHUTDOWN_COMPUTER.model" : core_funcs.shutdown,
    "VOLUME_CONTROL.model" : core_funcs.volume,
    "LOCK_COMPUTER.model" : core_funcs.lock
}

should_listen = False
prompts = [ "hey alice", "alice", "okay alice", "hey alex", "alex", "okay alex" ]

def parse_voice(speech_recognizer):
    global should_listen, prompts

    with sr.Microphone() as source:
        audio = speech_recognizer.listen(source)
    try:
        res = speech_recognizer.recognize_google(audio).lower()
        print("You said: " + res)

        for prompt in prompts:
            if res.startswith(prompt) and len(res) > len(prompt):
                res = res[ len(prompt): ]
                should_listen = True

        if should_listen:
            cross_check_models(res)

        should_listen = res in prompts

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

models = []
def load_models():
    global models
    model_list = glob.glob("../training/MODELS/*.model")
    print "Found %d models" % (len(model_list),)
    for model_name in model_list:
        with open(model_name, 'r') as MODEL_FILE:
            models.append(pickle.load(MODEL_FILE))
        print "Loaded model: %s" % (models[-1].name,)

def cross_check_models(sentence):
    print "Checking << %s >> with existing models..." % (sentence,)
    for model in models:
        if model.match(sentence):
            command_mapping[ model.name ](sentence)
        else:
            print "Did not match with %s" % (model.name,)

if __name__ == "__main__":
    load_models()
    r = sr.Recognizer()
    while True:
        parse_voice(r)

