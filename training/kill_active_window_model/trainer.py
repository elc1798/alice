import pickle
import os.path, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from alicized_models import CommandMatchingModel

MODEL_FILENAME = "KILL_ACTIVE_WINDOW.model"

def load_data():
    hot, cold = None, None
    with open("data/true.txt") as f:
        hot = f.read().strip().split('\n')
    with open("data/false.txt") as f:
        cold = f.read().strip().split('\n')
    return hot, cold

def get_classifier():
    if os.path.isfile(MODEL_FILENAME):
        print "Using existing model..."
        with open(MODEL_FILENAME, 'r') as MODEL_FILE:
            return pickle.load(MODEL_FILE)
    else:
        hot, cold = load_data()
        model = CommandMatchingModel( [hot, cold] , shuffle=True, train=True)

        with open(MODEL_FILENAME, 'w') as MODEL_FILE:
            pickle.dump(model, MODEL_FILE)
        return model

if __name__ == "__main__":
    text_classifier = get_classifier()
    while True:
        print "\tMatches: " + str( text_classifier.match( str(raw_input("Query: ")) ) )

