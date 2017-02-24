import random

import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

class CommandMatchingModel:

    def __init__(self, dataset, shuffle=True, train=False):
        """
        Creates an instance of the CommandMatchingModel.

        Params:
            dataset -   Python 2D List. Should have length 2, where the 0th
                        index contains the "True" data values and the 1st index
                        contains the "False" data values
            shuffle -   Boolean. If true, will shuffle the dataset using
                        random.shuffle. True by default.
            train   -   Boolean. If true, will train the classifier within the
                        constructor. False by default.
        """
        assert(len(dataset) == 2 and type(dataset[0]) == list and type(dataset[1]) == list)

        self.data = [ (i, "True") for i in dataset[0] ] + [ (i, "False") for i in dataset[1] ]
        if shuffle:
            random.shuffle(self.data)

        self.trained = False
        if train:
            try:
                self.train()
                self.trained = True
            except:
                pass

    def train(self):
        # Build training_set as a scikit-learn Bunch
        training_set = {
            "description" : "dataset for kill_active_window_model",
            "data" : [ t[0] for t in self.data ],
            "target_names" : ["True", "False"],
            "target" : [ t[1] for t in self.data ]
        }

        # Use Pipeline to train using SVM and Tfidf Feature Extraction
        self.classifier = Pipeline(
            [   ("vect", CountVectorizer()),
                ("tfidf", TfidfTransformer()),
                ("clsfr", SGDClassifier(loss="hinge", penalty="l2",
                    alpha=1e-3, n_iter=5, random_state=42)),
            ])
        _ = self.classifier.fit(training_set["data"], training_set["target"])

    def match(self, s):
        """
        Return Values:
            True -  s matches the classifier
            False - s does not match the classifier
            None -  the classifier has not been trained yet
        """
        if self.trained == False:
            print "Classifier has not been trained yet! Cannot match!"
            return None

        test = [ s.lower() ]
        predicted = self.classifier.predict(test)
        return predicted[0] == "True"

