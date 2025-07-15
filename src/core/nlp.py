import spacy
import datetime
import pytz
import parsedatetime as pdt

nlp = spacy.load("en_core_web_sm")
TZ = pytz.timezone("Asia/Kolkata")

def parse_intent(text: str) -> str:
    text_lower = text.lower()

    if any(word in text_lower for word in ["add", "schedule", "create", "set up"]):
        return "add_event"
    if any(word in text_lower for word in ["delete", "remove", "cancel"]):
        return "delete_event"
    if "next" in text_lower or "upcoming" in text_lower:
        return "get_next_events"
    if "all" in text_lower:
        return "get_all_events"
    if "today" in text_lower or "tomorrow" in text_lower or "next day" in text_lower:
        return "get_events_on_date"
    if any(word in text_lower for word in ["get", "what", "show"]):
        return "get_events_on_date"

    return "unknown"

def extract_event_info(text: str, allow_default_today: bool = True):
    doc = nlp(text)
    now = datetime.datetime.now(TZ)
    cal = pdt.Calendar()
    time_struct, parse_status = cal.parse(text, sourceTime=now.timetuple())

    if parse_status == 0:
        if allow_default_today:
            date_time = now + datetime.timedelta(hours=1)
            time_specified = False
        else:
            raise ValueError("Could not understand the date/time in your message.")
    else:
        date_time = datetime.datetime(*time_struct[:6], tzinfo=TZ)

        time_specified = False
        for token in doc:
            if token.ent_type_ == "TIME" or token.text.lower().endswith(("am", "pm")):
                time_specified = True
                break

    title = None
    for np in doc.noun_chunks:
        if any(kw in np.text.lower() for kw in ["appointment", "meeting", "call", "event"]):
            title = np.text.strip()
            break

    if not title:
        title = "Event"

    start_time = date_time
    end_time = start_time + datetime.timedelta(hours=1)

    return title.title(), start_time.isoformat(), end_time.isoformat(), time_specified



