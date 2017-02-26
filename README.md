# Alice

Digital Assistant for Linux, inspired by Cortana, Siri, Alexa, and Google Assistant

### Why did I decide to do this?

Because I got bored one day and started writing it.

### What technologies is this built on?

Alice is written in Python, with the libraries Numpy, Scikit, Scikit-learn, and
Google Speech Recognition.

### What can it do so far?

It can:
 - Shut down your computer
 - Lock your computer
 - Close whatever window you have currently active
 - Change your volume.
 - Open your web browser and URLs
 - Monitor incoming Facebook Messenger messages
 - Monitor CPU activity, memory usage, and temperatures
 - Monitors outdated packages in Apt and Pip

### Please expand the list of features!

The planned features are:

 - Opening files
 - Closing arbitrary windows that are open on your computer
 - Run system commands that you tell it to
 - Google service integration
 - Setting alarms
 - Checking the time
 - Checking the weather
 - Checking the news
 - Changing your screen brightness
 - Really anything else that I feel like adding...

### Why is it named Alice?

In the light novel / anime Sword Art Online: Alicization arc, Alice is a fully
sentient AI that truly mimics human-ness.

### Your code is crap, you boosted animal...

I know :( If you want to make any improvements / fixes, make a pull request
please!

### Ubuntu Notifications are broken...

Replace them with the default Gnome Notification Daemon:

1. Install notification-deamon (`sudo apt-get install notification-deamon`)
2. Open `/usr/share/dbus-1/services/org.freedesktop.Notifications.service` (Youcan backup this file if you plan to return to notify-osd later)
3. Change the 'Exec' line to `Exec = /usr/lib/notification-daemon/notification-daemon`
4. Save the file and restart computer

