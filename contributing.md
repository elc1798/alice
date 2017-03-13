### For development!

To install dependencies, you'll want to `pip install -r requirements.txt` and
run `setup.sh`.

You'll also need to make a directory in the root of the project called
`API_KEYS` and put a file called `google_creds.json` with your Google
credentials file inside (from the Google Developer Console)

To create a new command and it's training library you have to do 4 major steps:

 - Create a folder in `training/commands` with the naming scheme `COMMAND_NAME_DATA`
 - Populate the folder with `true.txt`, `false.txt`, and `tests.csv`, which are
   used during the machine learning training as the positive data, negative
   data, and unit tests, respectively.
 - Run `training/trainer.py` which is an automated pipeline that trains, tests,
   and stores the models
 - Add a new command to `app/commands`

How to add a new command to `app/commands`:

 - Make a new folder with the name of your command in it. The name of the
   directory really doesn't matter, but it should be descriptive.
 - Create a file called `__init__.py` in your folder. You can use the
   `__init__.py` file in any of the existing commands as a sample file.
 - The only things your `__init__.py` needs to work correctly are:
    - A variable called `TRIGGER_MODEL` containing a string with the name of the
      model that is supposed to trigger your command.
    - A variable called `FUNC` that is a pointer to a function that runs when
      your command is triggered. The method signature should take in 2
      arguments: `query` (the string that triggered it), and `**kwargs`, a
      dictionary of optional keyword arguments. `controllers` is a key that is
      commonly passed into `**kwargs`, and later on, SpaCy, `nlp` objects will
      be passed into it as well.

How to add a new controller to `app/controllers`:

 - Make a new folder in `app/controllers` with the name of your controller.
 - Create a file called `__init__.py`
 - The only thing your `__init__.py` file needs to work correctly are:
    - `NAME` (A variable that contains a unique identifier string for your
      controller)
    - `get_instance()` (A function that returns a (singleton, preferrably)
      instance of a class that represents your controller)

How to add a new monitor to `app/monitors`:
 - Make a new folder in `app/monitors` with the name of your new monitor.
 - Create a file called `__init__.py`
 - You will need both a `start()` and `stop()` method.
    - `start()` should create a background thread with whatever process you are
      running, as well as make it a daemon so it exits along with the main
      application.
    - `stop()` should handle any file closes, logging, etc. and is triggered
      when the main application ends using Python's `atexit` module.

