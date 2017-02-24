import os, sys, subprocess

import speech_recognition as sr
import core_funcs

command_mapping = {
    "exit" : sys.exit,
    "close window" : core_funcs.kill_active_window,
    "shutdown" : core_funcs.shutdown,
    "open file browser" : core_funcs.open_file_browser
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
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

if __name__ == "__main__":
    r = sr.Recognizer()
    while True:
        parse_voice(r)

