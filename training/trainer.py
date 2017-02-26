import pickle, csv
import os.path
import glob

from alicized_models import CommandMatchingModel
from alicized_models import GrammarMatchingModel
from alicized_models import OrdinalScaleModel

to_lower = lambda s : s.lower()

def load_data(data_folder):
    """
    Returns 2 lists: the hot list and cold list
    """
    print "[ DATA LOAD ] Loading data from %s..." % (data_folder,)
    hot, cold = None, None
    with open(os.path.join(data_folder, "true.txt")) as f:
        hot = map(to_lower, f.read().strip().split('\n'))
    with open(os.path.join(data_folder, "false.txt")) as f:
        cold = map(to_lower, f.read().strip().split('\n'))
    return hot, cold

def load_ordinal_scaler(data_folder):
    """
    Returns a dict, where the key is the ordinal value and the value is a list
    of samples.
    """
    data = {}
    print "[ DATA LOAD ] Loading data from %s..." % (data_folder,)
    data_samples = [ f for f in glob.glob(os.path.join(data_folder, "*.txt")) ]
    for fname in data_samples:
        with open(fname) as f:
            data[ os.path.basename(fname)[:-4] ] = map(to_lower, f.read().strip().split('\n'))
    return data

def has_custom_grammar(model_folder):
    return os.path.isfile(os.path.join(model_folder, "grammar.py")) and os.path.isfile(os.path.join(model_folder, "__init__.py"))

def has_custom_model(model_folder):
    return os.path.isfile(os.path.join(model_folder, "custom.py")) and os.path.isfile(os.path.join(model_folder, "__init__.py"))

def get_classifier(model_folder, dataset, use_old=False, ordinal_scalers=False):

    # The model name is the folder name without the _data at the end, in all
    # caps, and with the extension '.model'

    MODEL_FILENAME = model_folder[:-5].upper() + ".model"
    if ordinal_scalers:
        MODEL_FILENAME = "ORDINAL_SCALE_" + MODEL_FILENAME
    MODEL_PATH = os.path.join("MODELS", MODEL_FILENAME)

    if os.path.isfile(MODEL_PATH) and use_old:
        print "Using existing model..."
        with open(MODEL_PATH, 'r') as MODEL_FILE:
            return pickle.load(MODEL_FILE)
    else:
        g = None
        loss = "squared_hinge"
        penalty = "elasticnet"
        alpha = 1e-3
        n_iter = 5
        if has_custom_grammar(model_folder):
            tmp = __import__(model_folder + ".grammar").grammar.get_grammar()
            g = GrammarMatchingModel(rules=tmp)
        if has_custom_model(model_folder):
            tmp = __import__(model_folder + ".custom").custom.get_config()
            if "loss" in tmp:
                loss = tmp["loss"]
            if "penalty" in tmp:
                penalty = tmp["penalty"]
            if "alpha" in tmp:
                alpha = tmp["alpha"]
            if "n_iter" in tmp:
                n_iter = tmp["n_iter"]

        if ordinal_scalers:
            model = OrdinalScaleModel( dataset , shuffle=True, train=True,
                    name=MODEL_FILENAME,
                    loss=loss, penalty=penalty, alpha=alpha, n_iter=n_iter )
        else:
            model = CommandMatchingModel( dataset , shuffle=True, train=True,
                    name=MODEL_FILENAME, grammar=g,
                    loss=loss, penalty=penalty, alpha=alpha, n_iter=n_iter )

        with open(MODEL_PATH, 'w') as MODEL_FILE:
            pickle.dump(model, MODEL_FILE)
        return model

def get_training_list(ordinal_scalers=False):
    if ordinal_scalers:
        return [ path for path in glob.glob("ordinal_scalers/*_data") if
                os.path.isdir(path) and path != "_data" ]
    else:
        return [ path for path in glob.glob("*_data") if os.path.isdir(path)
                and path != "_data" ]

if __name__ == "__main__":

    training_list = get_training_list()
    # Data amplification

    amplified_data = {}
    for trainee in training_list:
        hot, cold = load_data(trainee)
        amplified_data[trainee] = [ hot, cold ]

    for trainee in training_list:
        for other in training_list:
            if trainee == other:
                continue
            amplified_data[trainee][1] += amplified_data[other][0] # Add the other's hot to our cold

    with open("nonsense.txt") as f:
        tmp = map(to_lower, f.read().strip().split('\n'))
        for trainee in amplified_data:
            amplified_data[trainee][1] += tmp

    training_list = get_training_list(ordinal_scalers=True)
    ordinal_scalers = {}
    for trainee in training_list:
        ordinal_scalers[os.path.basename(trainee)] = load_ordinal_scaler(trainee)

    print "\n\n"

    build_fail = [ False, "" ]

    for trainee in ordinal_scalers:
        model = get_classifier(trainee, ordinal_scalers[trainee], use_old=True,
                ordinal_scalers=True)
        
        failcount = 0
        num_tests = 0

        with open(os.path.join("ordinal_scalers", trainee, "test.csv")) as csvfile:
            tests = csv.reader(csvfile)
            for test in tests:
                if len(test) != 2:
                    continue
                num_tests += 1
                res = str(model.rate(test[0]))
                if res != test[1]:
                    failcount += 1
                    print "Failed on test: %s. Should be: %s, got %s instead." % (test[0], test[1], res)

        if failcount > 0:
            build_fail[0] = True
            build_fail[1] = "\n".join( (build_fail[1], "Errors in Model %s: Failed %d out of %d tests" % (trainee, failcount, num_tests)) )
        print "Model %s failed %d out of %d tests" % (trainee, failcount, num_tests)
        print "\n\n"

    for trainee in amplified_data:
        model = get_classifier(trainee, amplified_data[trainee], use_old=True)

        failcount = 0
        num_tests = 0

        with open(os.path.join(trainee, "test.csv")) as csvfile:
            tests = csv.reader(csvfile)
            for test in tests:
                if len(test) != 2:
                    continue
                num_tests += 1
                res = str(model.match(test[0]))
                if res != test[1]:
                    failcount += 1
                    print "Failed on test: %s. Should be: %s, got %s instead." % (test[0], test[1], res)

        with open(os.path.join(trainee, "true.txt")) as f:
            tests = f.read().strip().split("\n")
            for test in tests:
                if len(test) != 2:
                    continue
                num_tests += 1
                res = model.match(test)
                if res != True:
                    failcount += 1
                    print "Failed on test: %s. Should be: True, got %s instead." % (test, res)

        with open(os.path.join(trainee, "false.txt")) as f:
            tests = f.read().strip().split("\n")
            for test in tests:
                if len(test) != 2:
                    continue
                num_tests += 1
                res = model.match(test)
                if res != False:
                    failcount += 1
                    print "Failed on test: %s. Should be: False, got %s instead." % (test, res)

        if failcount > 0:
            build_fail[0] = True
            build_fail[1] = "\n".join( (build_fail[1], "Errors in Model %s: Failed %d out of %d tests" % (trainee, failcount, num_tests)) )
        print "Model %s failed %d out of %d tests" % (trainee, failcount, num_tests)
        print "\n\n"

    if build_fail[0]:
        print build_fail[1]
        assert(False)

