from services.gmail import get_unread_emails

emails = get_unread_emails()

for email in emails:
    print(email)