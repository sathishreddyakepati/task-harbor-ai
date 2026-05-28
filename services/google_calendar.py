from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
import os

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
    "https://www.googleapis.com/auth/gmail.readonly"
]


def get_calendar_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=creds
    )

    return service


def get_upcoming_events():

    service = get_calendar_service()

    now = datetime.utcnow().isoformat() + "Z"

    events_result = service.events().list(
        calendarId="primary",
        timeMin=now,
        maxResults=10,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    events = []

    for event in events_result.get("items", []):

        start = event["start"].get(
            "dateTime",
            event["start"].get("date")
        )

        try:

            if "T" in start:

                formatted_start = datetime.fromisoformat(
                    start.replace("Z", "+00:00")
                ).strftime(
                    "%b %d, %Y • %I:%M %p"
                )

            else:

                formatted_start = datetime.strptime(
                    start,
                    "%Y-%m-%d"
                ).strftime(
                    "%b %d, %Y"
                )

        except Exception:

            formatted_start = start

        events.append({
            "Event": event.get(
                "summary",
                "No Title"
            ),
            "Start": formatted_start
        })

    return events


def get_todays_events():

    events = get_upcoming_events()

    today = datetime.now().date()

    todays_events = []

    for event in events:

        try:

            date_part = event["Start"][:12]

            event_date = datetime.strptime(
                date_part,
                "%b %d, %Y"
            ).date()

            if event_date == today:
                todays_events.append(event)

        except Exception:
            pass

    return todays_events