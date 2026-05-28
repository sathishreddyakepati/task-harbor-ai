from services.google_calendar import get_calendar_service

service = get_calendar_service()

events = service.events().list(
    calendarId="primary",
    maxResults=20,
    singleEvents=True,
    orderBy="startTime"
).execute()

for event in events.get("items", []):
    print(event.get("summary"))