from __future__ import print_function

import datetime
import os.path

from dateutil.relativedelta import relativedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask
from sqlalchemy import text
from models import *

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def main() -> None:
    """
    Retrieve previous lessons from Google Calendar

    post: Previous events are retrieved and stored in database
    """

    calendarID = 'ou4mvifcr4sv41iopcpnlstg8c@group.calendar.google.com'
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)

        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        # 'Z' indicates UTC time
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        prev = datetime.datetime.utcnow() + relativedelta(months=-3)
        prev = prev.isoformat() + 'Z'

        events_result = service.events().list(calendarId=calendarID,
                                              timeMin=prev,
                                              timeMax=now, singleEvents=True,
                                              orderBy='startTime').execute()

        events = events_result.get('items', [])

        # Updates calendar data in database
        Previous.query.delete()
        for event in events:
            query_id = text(
                "SELECT id FROM users WHERE username =" + "'" + event[
                    'summary'] + "'")
            user_id = str(db.engine.execute(query_id).first())[1]
            start = event['start'].get('dateTime', event['start'].get('date'))
            start_date = start[0:10]
            start_time = start[11:25]
            end = event['end'].get('dateTime', event['end'].get('date'))
            end_time = end[11:25]
            attendees = event['attendees'][0]['email']
            try:
                confirmed = event['colorId'] is None
            except KeyError:
                confirmed = True
            # print(event)
            new_event = Previous(prev_user_id=user_id,
                                 prev_summary=event['summary'],
                                 prev_attendees=attendees,
                                 prev_date=start_date, prev_start=start_time,
                                 prev_datetime_start=start, prev_end=end_time,
                                 prev_datetime_end=end,
                                 prev_confirmed=confirmed)
            db.session.add(new_event)
        db.session.commit()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    print('Getting events from previous 3 months')
    with app.app_context():
        main()
