import os, sys, subprocess
import pickle
import glob

import speech_recognition as sr
import core_funcs

command_mapping = {
    "EXIT_ALICE" : core_funcs.exit,
    "KILL_ACTIVE_WINDOW.model" : core_funcs.kill_active_window,
    "SHUTDOWN_COMPUTER.model" : core_funcs.shutdown,
    "VOLUME_CONTROL.model" : core_funcs.volume
}

def parse_voice(speech_recognizer):
    with sr.Microphone() as source:
        print "Say something, I'm giving up on you~~~"
        audio = speech_recognizer.listen(source)
    try:
        res = speech_recognizer.recognize_google(audio)
        print("You said: " + res)
        if res in command_mapping:
            command_mapping[res]()
        else:
            cross_check_models(res)
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
    for model in models:
        if model.match(sentence):
            command_mapping[ model.name ](sentence)

if __name__ == "__main__":
    load_models()
    r = sr.Recognizer()
    while True:
        parse_voice(r)

