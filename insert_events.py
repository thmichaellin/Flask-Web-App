from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask import Flask
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


def main(summary: str, start: str, end: str, email: str) -> None:
    """
    Inserts new lesson into Google Calendar

    pre: summary is the username of a student: a str, start and end are
    lesson datetimes: strings, and email is the email of a student: a str

    post: a new event is inserted into Google Calendar with given information
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
        event = {
            'summary': summary,
            'colorId': 11,
            'start': {
                'dateTime': start,
            },
            'end': {
                'dateTime': end,
            },
            'attendees': [
                {'email': email},
            ],
        }

        # Insert new event to calendar
        service.events().insert(calendarId=calendarID,
                                body=event).execute()

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    with app.app_context():
        main('TEST', '2023-05-29T13:30:00+02:00', '2023-05-29T15:30:00+02:00',
             'test@email.com')
