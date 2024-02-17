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
    print(response)

if __name__ == "__main__":
    create_calendar("Test")
    # create_event("JAR App Prototype", "This is a new event", "2024-02-17T10:00:00", "2024-02-17T12:00:00", calendar_id="c_5e6dce2085b61bab7cdfb825b1ca1040501b6938ff5aa2cdee4ae45acd44722c@group.calendar.google.com")