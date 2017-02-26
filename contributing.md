### For development!

To install dependencies, you'll want to `pip install -r requirements.txt` and
run `setup.sh`.

To create a new command and it's training library you have to do 4 major steps:

 - Create a folder in `training/` with the naming scheme `COMMAND_NAME_DATA`
 - Populate the folder with `true.txt`, `false.txt`, and `tests.csv`, which are
   used during the machine learning training as the positive data, negative
   data, and unit tests, respectively.
 - Run `training/trainer.py` which is an automated pipeline that trains, tests,
   and stores the models
 - Add a command to the `CommandActuator` class in `app/core_funcs.py`

To create a new monitor or background process, create a new file in
`app/services` and run a new thread in the global scope. To add it to alice,
import it in the `main` function in `app/app.py`.
