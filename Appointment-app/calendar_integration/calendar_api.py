from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_free_slots():
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('calendar', 'v3', credentials=creds)
    # Fetch free slots logic here
    return ["2025-06-07 10:00", "2025-06-07 14:00"]

def book_appointment(slot):
    # Create event in Google Calendar
    pass
