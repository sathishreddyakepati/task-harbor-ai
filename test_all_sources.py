# test_all_sources.py

from services.notion import get_tasks
from services.google_calendar import get_upcoming_events
from services.gmail import get_unread_emails

print("Tasks:", len(get_tasks()))
print("Events:", len(get_upcoming_events()))
print("Emails:", len(get_unread_emails()))