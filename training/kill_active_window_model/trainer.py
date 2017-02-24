# import spacy
import random
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier

# nlp = spacy.load('en')

f = open("data/true.txt")
g = open("data/false.txt")

# hot = [ nlp(unicode(s)) for s in f.read().strip().split('\n') ]
# cold = [ nlp(unicode(s)) for s in g.read().strip().split('\n') ]

hot = f.read().strip().split('\n')
cold = g.read().strip().split('\n')

f.close()
g.close()

# Build training_set as a scikit-learn Bunch

data = [ (i, "True") for i in hot ] + [ (i, "False") for i in cold ]
random.shuffle(data)

training_set = {
    "description" : "dataset for kill_active_window_model",
    "data" : [ t[0] for t in data ],
    "target_names" : ["True", "False"],
    "target" : [ t[1] for t in data ]
}

# print training_set["data"][:5]
# print training_set["target"][:5]

count_vect = CountVectorizer()
# X_train_counts = count_vect.fit_transform(training_set["data"])
# print X_train_counts.shape
# tfidf_transformer = TfidfTransformer()

text_classifier = Pipeline(
    [   ("vect", CountVectorizer()),
        ("tfidf", TfidfTransformer()),
        ("clsfr", SGDClassifier(loss="hinge", penalty="l2",
            alpha=1e-3, n_iter=5, random_state=42)),
    ])

_ = text_classifier.fit(training_set["data"], training_set["target"])

# sanity_check = text_classifier.predict(training_set)
# print np.mean(sanity_check == training_set["target"])

while True:
    test = [ str(raw_input("Test Query: ")).lower() ]
    predicted = text_classifier.predict(test)
    print "\t\tGuess: " + str(predicted[0])



