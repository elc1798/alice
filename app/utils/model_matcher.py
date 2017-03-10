class ModelMatcher:

    def __init__(self, models, log_func=default_log):
        self.models = models
        self.log_func = logger_func

    def get_matches(self, query):
        query = query.strip().lower()

        matches = []
        self.log_func("Checking << %s >> with existing models..." % (sentence,))
        for model in models:
            if model.match(query):
                self.log_func("Matched with %s" % (model.name,))
                matches.append(model.name)
            else:
                self.log_func("Did not match with %s" % (model.name,), tolerance=2)

        return matches

def default_log(s, tolerance=0):
    print s

