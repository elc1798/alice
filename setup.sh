# Installs required packages

# Ubuntu 14

sudo apt-get install speech-dispatcher
sudo apt-get install libportaudio-dev libportaudio2 libportaudio0 libportaudiocpp0
sudo apt-get install libasound-dev
sudo apt-get install portaudio19-dev libjack-dev libjack0

# Ubuntu 16

sudo apt-get install speech-dispatcher
sudo apt-get install libportaudio2 libportaudio0
sudo apt-get install libasound2-dev
sudo apt-get install libjack-jackd2-dev
sudo apt-get install portaudio19-dev

# All

sudo pip install -U SpeechRecognition numpy pyaudio sklearn matplotlib pandas scipy
sudo pip install -U spacy

sudo python -m spacy.en.download all

