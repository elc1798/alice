import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants
import urllib2, json

NEWS_API_URL = "https://newsapi.org/v1/articles?source=the-new-york-times&sortBy=top&apiKey=3ca58b6ade8f4fc69988ed4d497a5d79"

NUM_ARTICLES = 5

def get_news(query, controllers):
    jstr = urllib2.urlopen(url).read()
    ts = json.loads( jstr )
    for i in range(NUM_ARTICLES):
        headline = ( str(i+1) +  ". " + ts['articles'][i]['title'] )
        headline = ''.join([i if ord(i) < 128 else ' ' for i in headline])
        print headline
        os.system(constants.DISPLAY_NOTIFICATION % (headline,))

TRIGGER_MODEL = "GET_NEWS.model"
FUNC = get_news

