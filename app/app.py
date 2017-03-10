import os, sys, subprocess
import pickle, glob
import argparse
import getpass

from utils import alice_receiver as ar
from commander import Commander

# Version Control Constants
APPLICATION_NAME = "Alice"
APPLICATION_RELEASE = 0
APPLICATION_REVISION = 136

VERBOSITY = 0
should_listen = False

alice = None

def log(s, tolerance=1):
    global VERBOSITY

    if VERBOSITY >= tolerance:
        print(s)

def main():
    global use_voice, alice

    alice = Commander(log_func=log)

    if use_voice:
        recognize = ar.AliceReceiver(str(raw_input("Alice login: ")),
                str(getpass.getpass()), alice.parse_query, debug=False)
        print("Alice is listening on Facebook!")
        recognize.listen()
    else:
        while True:
            query = str(raw_input("alice > "))
            alice.parse_query(query)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Alice - Linux Virtual Assistant")
    parser.add_argument("--use-voice", "-V", action="store_true")
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('--version', action='version', version="%s %d.%d" %
            (APPLICATION_NAME, APPLICATION_RELEASE, APPLICATION_REVISION))

    args = parser.parse_args()

    use_voice = args.use_voice
    VERBOSITY = args.verbose

    main()

