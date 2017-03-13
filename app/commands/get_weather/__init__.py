import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

import urllib2, json
import pyowm

URL = "http://freegeoip.net/json/"
API_KEY = "70e52321050523bb149227183e2ec5e5"

def get_weather(query, **kwargs):
    f = urllib2.urlopen(URL)
    json_string = f.read()
    f.close()
    location = json.loads(json_string)
    location_city = location['city']
    place = 'location[\'city\']' + ", " + location['country_code']
    owm = pyowm.OWM(API_KEY)
    w = owm.weather_at_place(place).get_weather()
    temp = (w.get_temperature('fahrenheit')['temp_max'] +w.get_temperature('fahrenheit')['temp_min']) / 2 
    weather = "The temperature today is " + str(temp) + " degrees fahrenheit"
    os.system(constants.DISPLAY_NOTIFICATION % (weather,))

TRIGGER_MODEL = "GET_WEATHER.model"
FUNC = get_weather
