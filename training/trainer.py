import pickle, csv
import os.path
import glob
import argparse
import numpy as np

from alicized_models import CommandMatchingModel
from alicized_models import GrammarMatchingModel
from alicized_models import OrdinalScaleModel

USE_OLD = False

COMMANDS_GLOB_PATTERN = "data/commands/*_data"
ORDINAL_SCALERS_GLOB_PATTERN = "data/ordinal_scalers/*_data"
MODEL_FILE_EXTENSION = ".model"
LOSS_FUNCTIONS = [
    "hinge",
    "log",
    "modified_huber",
    "squared_hinge",
    "perceptron",
    "squared_loss",
    "huber",
    "epsilon_insensitive",
    "squared_epsilon_insensitive"
]
PENALTY_FUNCTIONS = [ "none", "l2", "l1", "elasticnet" ]

TRAIN_PAIRS = [
    ( loss, penalty )
    for loss in LOSS_FUNCTIONS
    for penalty in PENALTY_FUNCTIONS
]

def load_data(dataset_path):
    """
    Returns the hot list (true cases) and cold list (false cases)

    Args:
        dataset_path:   The path to the folder containing the data files
    """
    print "[ DATA LOAD ] Loading data from %s..." % (dataset_path,)

    data = {}
    sets = glob.glob("%s/*.txt" % (dataset_path,))
    for fname in sets:
        with open(fname, 'r') as f:
            set_name = os.path.basename(fname).split(".")[0]
            contents = f.read().strip().lower().split("\n")
            data[set_name] = [ i for i in contents if len(i) > 0 ]
    return data

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

def get_model_name(dataset_path):
    """
    Returns the model's name given its dataset_path

    Args:
        dataset_path: path to the model's dataset

    Returns:
        The model's name as a string
    """
    # The model name is the folder name without the _data at the end, in all
    # caps, and with the extension '.model'
    return os.path.basename(dataset_path)[:-5].upper() + MODEL_FILE_EXTENSION

def get_model_path(dataset_path):
    """
    Returns the model's path given its dataset_path
    """
    assert(os.path.dirname(dataset_path).startswith("data/"))
    return os.path.join(
        os.path.dirname(
            dataset_path.replace("data", "models", 1)
        ), get_model_name(dataset_path)
    )

def get_existing_classifier(model_folder, dataset, use_old=False):
    MODEL_FILENAME = get_model_name(model_folder)
    MODEL_PATH = get_model_path(model_folder)

    if os.path.isfile(MODEL_PATH) and use_old:
        print "Using existing model..."
        with open(MODEL_PATH, 'r') as MODEL_FILE:
            return pickle.load(MODEL_FILE)
    else:
        return None

def get_classifiers(model_folder, dataset, ordinal_scaler=False):
    global USE_OLD
    g = None
    alpha = 1e-3
    n_iter = 5

    if USE_OLD:
        model = None
        with open(get_model_path(model_folder), 'r') as MODEL_FILE:
            model = pickle.load(MODEL_FILE)
            return [ model ]

    model_class = CommandMatchingModel
    if ordinal_scaler:
        model_class = OrdinalScaleModel

    models = []
    for loss in LOSS_FUNCTIONS:
        for penalty in PENALTY_FUNCTIONS:
            model = model_class(
                dataset,
                shuffle=True,
                train=True,
                name=get_model_name(model_folder),
                grammar=g,
                loss=loss,
                penalty=penalty,
                alpha=alpha,
                n_iter=n_iter
            )

            models.append(model)
    return models

def get_datasets(glob_pattern):
    """
    Gets a list of paths to dataset directories using a globbing pattern

    Args:
        glob_pattern:   A globbing pattern for directory tree traversal,
                        i.e. **/filename, subdir/*.txt, subdir/*_data

    Returns:
        A Python list of strings, representing directory paths
    """
    return [
        path
        for path in glob.glob(glob_pattern)
        if os.path.isdir(path)
    ]

def get_command_data_list():
    """
    Gets a list of paths to command datasets using get_datasets
    """
    return get_datasets(COMMANDS_GLOB_PATTERN)

def get_ordinal_scaler_data_list():
    """
    Gets a list of paths to ordinal scaler datasets using get_datasets
    """
    return get_datasets(ORDINAL_SCALERS_GLOB_PATTERN)

def test_model(test_func, tests, correct):
    failcount = 0
    error_messages = []
    for i in range(len(tests)):
        res = test_func(tests[i])
        if res != correct[i]:
            error_messages.append(
                "Failed test '%s': Got '%r', should be '%r'" % (tests[i], res, correct[i])
            )
            failcount += 1
    return failcount, "\n".join(error_messages)

def get_amplified_data_from_training_list(training_list, ordinal_scaler=False):
    amplified_data = {}
    for trainee in training_list:
        amplified_data[trainee] = load_data(trainee)

    if not ordinal_scaler:
        for trainee in training_list:
            for other in training_list:
                if trainee == other:
                    continue
                amplified_data[trainee]["false"] += amplified_data[other]["true"]
    return amplified_data

def get_best_model(trainee, models, test_cases, correct, build_fail=[False,"",0,0], ordinal_scaler=False):
    global USE_OLD

    # Build testing data and variables
    failcounts = []
    error_messages = []

    num_tests = len(test_cases)

    # Run tests with each possible model and keep track of the best one
    min_index = -1
    min_value = float("inf")
    for model in models:
        func = model.rate if ordinal_scaler else model.match
        f_count, message = test_model(func, test_cases, correct)
        failcounts.append(f_count)
        error_messages.append(message)
        if failcounts[-1] < min_value:
            min_index = len(failcounts) - 1
            min_value = failcounts[-1]

    if min_value > 0:
        build_fail[0] = True
        build_fail[1] = "\n".join(
            (
                build_fail[1],
                "Errors in Model %s: Failed %d out of %d tests" % (trainee, min_value, num_tests)
            )
        )
        build_fail[2] += min_value
        build_fail[3] += num_tests

    if failcounts[min_index] > 0:
        print "\n", error_messages[min_index]
    print "Model %s failed %d out of %d tests" % (trainee, min_value, num_tests)

    # Assert that our fail rate is small
    assert(float(min_value) / float(num_tests) * 100 < 0.5)

    # Save the best model
    if not USE_OLD:
        with open(get_model_path(trainee), 'w') as MODEL_FILE:
            pickle.dump(models[min_index], MODEL_FILE)

    return build_fail

def train_commands():
    global USE_OLD

    amplified_data = get_amplified_data_from_training_list(get_command_data_list())

    with open("nonsense.txt") as f:
        tmp = f.read().strip().lower().split('\n')
        for trainee in amplified_data:
            amplified_data[trainee]["false"] += tmp

    build_fail = [ False, "", 0, 0 ]

    for trainee in amplified_data:
        models = get_classifiers(trainee, amplified_data[trainee])

        test_cases = []
        correct = []
        with open(os.path.join(trainee, "test.csv")) as csvfile:
            tests = csv.reader(csvfile)
            for test in tests:
                if len(test) != 2:
                    continue
                test_cases.append(test[0].strip())
                correct.append(test[1].strip().lower() == "true")

        test_cases += amplified_data[trainee]["true"]
        correct += [ True ] * len(amplified_data[trainee]["true"])

        test_cases += amplified_data[trainee]["false"]
        correct += [ False ] * len(amplified_data[trainee]["false"])

        build_fail = get_best_model(trainee, models, test_cases, correct, build_fail=build_fail)

    if build_fail[0]:
        print build_fail[1]

    return build_fail[-2:]

def train_ordinal_scalers():
    global USE_OLD

    amplified_data = get_amplified_data_from_training_list(
        get_ordinal_scaler_data_list(),
        ordinal_scaler=True
    )

    build_fail = [ False, "", 0, 0 ]

    for trainee in amplified_data:
        models = get_classifiers(
            trainee,
            amplified_data[trainee],
            ordinal_scaler=True
        )

        test_cases = []
        correct = []
        with open(os.path.join(trainee, "test.csv")) as csvfile:
            tests = csv.reader(csvfile)
            for test in tests:
                if len(test) != 2:
                    continue
                test_cases.append(test[0].strip().lower())
                correct.append(int(test[1].strip().lower()))

        for ordinality in amplified_data[trainee]:
            test_cases += amplified_data[trainee][ordinality]
            correct += [ int(ordinality) ] * len(amplified_data[trainee][ordinality])

        build_fail = get_best_model(trainee, models, test_cases, correct,
                build_fail=build_fail, ordinal_scaler=True)

    if build_fail[0]:
        print build_fail[1]

    return build_fail[-2:]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Granular Price Risk Analyzer")
    parser.add_argument("--train-commands", "-c", action="store_true", help="Train all the commands")
    parser.add_argument("--train-ord-scalers", "-o", action="store_true", help="Train all the ordinal scalers")
    parser.add_argument("--use-old", "-u", action="store_true", help="Test pre-trained models rather than re-train")

    args = parser.parse_args()

    error_rate = np.zeros(2)

    if args.use_old:
        USE_OLD = True
    if args.train_commands:
        error_rate += np.array(train_commands())
    if args.train_ord_scalers:
        error_rate += np.array(train_ordinal_scalers())

    error_percentage = (float(error_rate[0]) / float(error_rate[1])) * 100
    print "Fail rate: %f%%" % (error_percentage,)
    assert(error_rate[1] == 0 or error_percentage < 0.5)

