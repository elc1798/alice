import sys, os
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(CURRENT_DIR, ".."))
from utils import google as goog
sys.path.insert(0, os.path.join(CURRENT_DIR, "..", ".."))
import constants

TRIGGER_MODEL = "GOOGLE_MAIL_LIST_MAIL.model"
FUNC = lambda query, controllers: goog.list_mail(["UNREAD"])

