from fastapi import APIRouter
from src.models.message import MessageRequest, MessageResponse
from src.core.nlp import parse_intent, extract_event_info
from src.core.calendar_api import (
    get_events_on_date,
    get_event_at_time,
    add_event,
    delete_event,
    get_next_events,
    get_all_events,
)
import datetime

router = APIRouter()

HELP_MESSAGE = (
    "Sorry, I didn't understand that. 🤖\n"
    "You can say things like:\n"
    "- Get tomorrow's events\n"
    "- Get event tomorrow 6 PM\n"
    "- Add a meeting tomorrow at 3 PM\n"
    "- Delete event tomorrow 6 PM\n"
    "- Delete events tomorrow\n"
    "- What are the next events?\n"
    "- Show me all events\n"
)

@router.post("/chat", response_model=MessageResponse)
def chatbot_handler(request: MessageRequest) -> MessageResponse:
    intent = parse_intent(request.text)

    try:
        if intent in ["get_events_on_date", "delete_event"]:
            _, start_iso, _, time_specified = extract_event_info(request.text)
            start_dt = datetime.datetime.fromisoformat(start_iso)

            if intent == "get_events_on_date":
                if time_specified:
                    events = get_event_at_time(start_dt.date(), start_dt.time())
                    return {"response": f"Events at {start_dt.strftime('%d/%m/%Y %H:%M:%S')}: {events}"}
                else:
                    events = get_events_on_date(start_dt.date())
                    return {"response": f"Events on {start_dt.strftime('%d/%m/%Y')}: {events}"}

            elif intent == "delete_event":
                time_to_match = start_dt.time() if time_specified else None
                result = delete_event(date=start_dt.date(), time_to_match=time_to_match)
                return {"response": result}

        elif intent == "add_event":
            title, start_iso, end_iso, _ = extract_event_info(request.text)
            add_event(title, start_iso, end_iso)
            start_dt = datetime.datetime.fromisoformat(start_iso)
            return {"response": f"✅ Event '{title}' added at {start_dt.strftime('%d/%m/%Y %H:%M:%S')}"}

        elif intent == "get_next_events":
            events = get_next_events()
            return {"response": f"📅 Next events:\n{events}"}

        elif intent == "get_all_events":
            events = get_all_events()
            return {"response": f"📅 All events:\n{events}"}

    except ValueError as e:
        return {"response": str(e)}

    return {"response": HELP_MESSAGE}


