import random
import pickle
import os.path

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

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
        # Get data
        hot, cold = load_data()

        # Build training_set as a scikit-learn Bunch
        data = [ (i, "True") for i in hot ] + [ (i, "False") for i in cold ]
        random.shuffle(data)

        training_set = {
            "description" : "dataset for kill_active_window_model",
            "data" : [ t[0] for t in data ],
            "target_names" : ["True", "False"],
            "target" : [ t[1] for t in data ]
        }

        text_classifier = Pipeline(
            [   ("vect", CountVectorizer()),
                ("tfidf", TfidfTransformer()),
                ("clsfr", SGDClassifier(loss="hinge", penalty="l2",
                    alpha=1e-3, n_iter=5, random_state=42)),
            ])
        _ = text_classifier.fit(training_set["data"], training_set["target"])

        with open(MODEL_FILENAME, 'w') as MODEL_FILE:
            pickle.dump(text_classifier, MODEL_FILE)
        return text_classifier

if __name__ == "__main__":
    text_classifier = get_classifier()
    while True:
        test = [ str(raw_input("Test Query: ")).lower() ]
        predicted = text_classifier.predict(test)
        print "\t\tGuess: " + str(predicted[0])

