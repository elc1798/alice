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

### Please expand the list of features!

The planned features are:

 - Opening files
 - Closing arbitrary windows that are open on your computer
 - Run system commands that you tell it to
 - Setting alarms
 - Launching Google maps and getting directions on the fly
 - Checking the weather
 - Checking the news
 - Changing your screen brightness
 - Really anything else that I feel like adding...

### Why is it named Alice?

In the light novel / anime Sword Art Online: Alicization arc, Alice is a fully
sentient AI that truly mimics human-ness.

### Your code is bad, you boosted animal...

I know :( If you want to make any improvements / fixes, make a pull request
please!

### Ubuntu Notifications are broken...

Yeah, it's a known bug, but `notify-osd` cannot stack messages, and will display
them in a queue. Sorry, it's not my fault :(

