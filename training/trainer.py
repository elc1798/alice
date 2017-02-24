import pickle, csv
import os.path
import glob

from alicized_models import CommandMatchingModel

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

def get_classifier(model_folder, dataset):

    # The model name is the folder name without the _data at the end, in all
    # caps, and with the extension '.model'
    MODEL_FILENAME = model_folder[:-5].upper() + ".model"
    MODEL_PATH = os.path.join("MODELS", MODEL_FILENAME)

    if os.path.isfile(MODEL_PATH):
        print "Using existing model..."
        with open(MODEL_PATH, 'r') as MODEL_FILE:
            return pickle.load(MODEL_FILE)
    else:
        model = CommandMatchingModel( dataset , shuffle=True, train=True, name=MODEL_FILENAME)

        with open(MODEL_PATH, 'w') as MODEL_FILE:
            pickle.dump(model, MODEL_FILE)
        return model

def get_training_list():
    return [ path for path in glob.glob("*_data") if os.path.isdir(path) and path != "_data" ]

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

    print amplified_data

    build_fail = [ False, "" ]

    for trainee in amplified_data:
        model = get_classifier(trainee, amplified_data[trainee])

        failcount = 0
        num_tests = 0

        with open(os.path.join(trainee, "test.csv")) as csvfile:
            tests = csv.reader(csvfile)
            for test in tests:
                num_tests += 1
                res = str(model.match(test[0]))
                if res != test[1]:
                    failcount += 1
                    print "Failed on test: %s. Should be: %s, got %s instead." % (test[0], test[1], res)

        if failcount > 0:
            build_fail[0] = True
            build_fail[1] = "\n".join( (build_fail[1], "Errors in Model %s" % (trainee,)) )
        print "Model %s failed %d out of %d tests" % (trainee, failcount, num_tests)

    if build_fail[0]:
        print build_fail[1]
        assert(False)

