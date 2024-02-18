from pprint import pprint
from Google import Create_Service

CLIENT_SECRET_FILE = "resources/client_secret_342844313175-aim4c6vmoqflanpso2d7svea0dddmlpp.apps.googleusercontent.com.json"
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
def create_calendar(title="New JAR"):
    request_body = {
        "summary": title
    }

    response = service.calendars().insert(body=request_body).execute()
    # print(response)

    # get the calendar id and the public url
    calendar_id = response["id"]

    return calendar_id

def create_event(title, description, start_time, end_time, calendar_id="primary"):
    event = {
        "summary": title,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": "America/Los_Angeles"
        },
        "end": {
            "dateTime": end_time,
            "timeZone": "America/Los_Angeles"
        }
    }

    response = service.events().insert(calendarId=calendar_id, body=event).execute()
    # print(response)

    return response

def delete_event(calendar_id, event_id):
    """ Delete an event from the calendar """
    service.events().delete(calendarId=calendar_id, eventId=event_id).execute()

def list_events(calendar_id):
    """ Return a list of all event_id in the calendar"""
    response = service.events().list(calendarId=calendar_id).execute() 

    events = []
    for event in response["items"]:
        events.append(calendar_id+'-----'+event["id"])

    return events

def edit_event_title(calendar_id, event_id, new_title):
    """ Edit the title of an event """
    event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
    event["summary"] = new_title
    service.events().update(calendarId=calendar_id, eventId=event_id, body=event).execute()

def edit_calendar_title(calendar_id, new_title):
    """ Edit the title of a calendar """
    calendar = service.calendars().get(calendarId=calendar_id).execute()
    calendar["summary"] = new_title
    service.calendars().update(calendarId=calendar_id, body=calendar).execute()

def get_event_info(event_id):
    calendar_id, internal_event_id = event_id.split("-----")
    response = service.events().get(calendarId=calendar_id, eventId=internal_event_id).execute()
    # print(response)

    start_time = response["start"]["dateTime"]
    end_time = response["end"]["dateTime"]
    title = response["summary"]

    return title, start_time, end_time

if __name__ == "__main__":
    create_calendar("Test")
    # create_event("JAR App Prototype", "This is a new event", "2024-02-17T10:00:00", "2024-02-17T12:00:00", calendar_id="c_5e6dce2085b61bab7cdfb825b1ca1040501b6938ff5aa2cdee4ae45acd44722c@group.calendar.google.com")