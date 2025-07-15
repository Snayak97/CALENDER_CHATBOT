from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from src.config import TOKEN_PATH, SCOPES
import datetime
import pytz

TZ = pytz.timezone("Asia/Kolkata")

def format_dt(dt: datetime.datetime) -> str:
    return dt.strftime("%d/%m/%Y %H:%M:%S")

def get_calendar_service():
    creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    return build("calendar", "v3", credentials=creds)

def get_events_on_date(date: datetime.date) -> str:
    service = get_calendar_service()
    time_min = datetime.datetime.combine(date, datetime.time.min, tzinfo=TZ).isoformat()
    time_max = datetime.datetime.combine(date, datetime.time.max, tzinfo=TZ).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if not events:
        return f"No events on {date.strftime('%d/%m/%Y')}."

    return "\n".join(
        f"📌 {event.get('summary', 'No Title')} at {format_dt(datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(TZ))}"
        for event in events
    )

def get_event_at_time(date: datetime.date, time: datetime.time) -> str:
    service = get_calendar_service()
    time_min = datetime.datetime.combine(date, datetime.time.min, tzinfo=TZ).isoformat()
    time_max = datetime.datetime.combine(date, datetime.time.max, tzinfo=TZ).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    matches = []
    for event in events:
        start_dt = datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(TZ)
        if abs((start_dt.hour * 60 + start_dt.minute) - (time.hour * 60 + time.minute)) <= 5:
            matches.append(f"📌 {event['summary']} at {format_dt(start_dt)}")

    if not matches:
        return f"No events found at {time.strftime('%H:%M')} on {date.strftime('%d/%m/%Y')}."
    return "\n".join(matches)

def add_event(title: str, start_time: str, end_time: str):
    service = get_calendar_service()
    event = {
        'summary': title,
        'start': {'dateTime': start_time, 'timeZone': 'Asia/Kolkata'},
        'end': {'dateTime': end_time, 'timeZone': 'Asia/Kolkata'},
    }
    service.events().insert(calendarId='primary', body=event).execute()

def delete_event(title: str = None, date: datetime.date = None, time_to_match: datetime.time = None) -> str:
    service = get_calendar_service()
    if not date:
        date = datetime.datetime.now(TZ).date()

    time_min = datetime.datetime.combine(date, datetime.time.min, tzinfo=TZ).isoformat()
    time_max = datetime.datetime.combine(date, datetime.time.max, tzinfo=TZ).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=time_min,
        timeMax=time_max,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    deleted_count = 0

    for event in events:
        start_dt = datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(TZ)

        if time_to_match and abs((start_dt.hour * 60 + start_dt.minute) - (time_to_match.hour * 60 + time_to_match.minute)) > 5:
            continue

        service.events().delete(calendarId='primary', eventId=event['id']).execute()
        deleted_count += 1

    if deleted_count > 0:
        return f"✅ Deleted {deleted_count} event(s) on {date.strftime('%d/%m/%Y')}."
    else:
        return f"⚠️ No matching event(s) found on {date.strftime('%d/%m/%Y')}."

def get_next_events(max_results: int = 10) -> str:
    service = get_calendar_service()
    now = datetime.datetime.now(TZ).isoformat()

    events_result = service.events().list(
        calendarId='primary',
        timeMin=now,
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if not events:
        return "No upcoming events found."

    return "\n".join(
        f"📌 {event.get('summary', 'No Title')} at {format_dt(datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(TZ))}"
        for event in events
    )

def get_all_events(max_results: int = 50) -> str:
    service = get_calendar_service()

    events_result = service.events().list(
        calendarId='primary',
        maxResults=max_results,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    if not events:
        return "No events found on the calendar."

    return "\n".join(
        f"📌 {event.get('summary', 'No Title')} at {format_dt(datetime.datetime.fromisoformat(event['start']['dateTime']).astimezone(TZ))}"
        for event in events
    )


