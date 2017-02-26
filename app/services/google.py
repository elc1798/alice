from __future__ import print_function
import httplib2, os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = '../../API_KEYS/google_creds.json'
APPLICATION_NAME = 'Alice'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        print("Directory does not exist :(")
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def ShowEvents(s):
    time_max = GetTimeMax(s)
    num_of_events = 20
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting up to', num_of_events, 'events')
    eventsResult = service.events().list(
        calendarId='primary', timeMin=now, maxResults=num_of_events,
        singleEvents=True, timeMax=time_max,
        orderBy='startTime').execute()
    events = eventsResult.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

def GetTimeMax(s):
    date_utc = datetime.datetime.now()
    date_utc = date_utc.replace(hour=23, minute=59, second=59)
    time_delta = datetime.timedelta(days=0)

    if s[0] == 'this':
        print('this')
        s.pop(0)
    if s[0] == 'next':
        print('next')
        time_delta += datetime.timedelta(weeks=1)
        s.pop(0)

    date_utc = date_utc + time_delta

    if s == 'today' or s[0] == '' or s[0] == 'today':
        print('today')
        return date_utc.isoformat() + 'Z'
    if s[0] == 'day':
        print('day')
        return date_utc.isoformat() + 'Z'
    if s[0] == 'tomorrow':
        print('tomorrow')
        date_utc = date_utc + datetime.timedelta(days=1)
        return date_utc.isoformat() + 'Z'
    if s[0] == 'week':
        print('week')
        date_utc = date_utc + datetime.timedelta(weeks=1)
        return date_utc.isoformat() + 'Z'
    if s[0] == 'month':
        print('month')
        date_utc = date_utc + datetime.timedelta(weeks=4)
        return date_utc.isoformat() + 'Z'

    day_now = datetime.datetime.today().weekday()

    if s[0] == 'monday':
        print('monday')
        day_diff = day_now
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'
    elif s[0] == 'tuesday':
        print('tuesday')
        day_diff = abs(day_now - 1)
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'
    elif s[0] == 'wednesday':
        print('wednesday')
        day_diff = abs(day_now - 2)
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'
    elif s[0] == 'thursday':
        print('thursday')
        day_diff = abs(day_now - 3)
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'
    elif s[0] == 'friday':
        print('friday')
        day_diff = abs(day_now - 4)
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'
    elif s[0] == 'saturday':
        print('saturday')
        day_diff = abs(day_now - 5)
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'
    elif s[0] == 'sunday':
        print('sunday')
        day_diff = abs(day_now - 6)
        date_utc = date_utc + datetime.timedelta(days=day_diff)
        return date_utc.isoformat() + 'Z'

#if __name__ == '__main__':
#    main()
