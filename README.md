# Alice

Digital Assistant for Linux (and Mac!), inspired by Cortana, Siri, Alexa, and Google Assistant

### Why did I decide to do this?

Because I thought it was a cool idea, I was bored, and also it was HackIllinois.

### What technologies is this built on?

Alice is written in Python, with the libraries Numpy, Scikit, Scikit-learn, and
Google Speech Recognition (on Android).

### What can it do so far?

It can:
 - Shut down your computer
 - Lock your computer
 - Close whatever window you have currently active
 - Change your volume.
 - Control the music that's playing (Rhythmbox on Ubuntu, Spotify on Mac OSX)
 - Open your web browser and URLs
 - Monitor incoming Facebook Messenger messages
 - Monitor CPU activity, memory usage, and temperatures
 - Monitors outdated packages in Apt and Pip
 - Checking the time
 - Google service integration for Gmail (checking inbox) and Calendar (checking
   events)
 - Being able to create Google Calendar events
 - Checking the weather
 - Checking the news

### Please expand the list of features!

The planned features are:

 - Opening files
 - Closing arbitrary windows that are open on your computer
 - Run system commands that you tell it to
 - Setting alarms
 - Launching Google maps and getting directions on the fly
 - Able to send emails
 - Changing your screen brightness
 - Really anything else that I feel like adding...

### Why is it named Alice?

It's the name of a character in a light novel who's the first sentient AI.

### Your code is bad, you boosted animal...

I know :( If you want to make any improvements / fixes, make a pull request
please!

### Ubuntu Notifications are broken...

Yeah, it's a known bug, but `notify-osd` cannot stack messages, and will display
them in a queue. Sorry, it's not my fault :(

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

### Licensing

This project has been licensed with the MIT license due to its simplicity,
simple language, and the fact that the point of the project was to provide a
free alternative to the digital assistants that are available on the rest of the
popular operating systems. Due to this project's open source nature, there
should be no warranty or guarantees of some working product, as changes will be
constantly made.

