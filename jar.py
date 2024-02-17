import json

from notion import create_database, create_page
from google_calendar import create_calendar, create_event

def create_jar(title):
    # Create a new JAR in Notion
    create_database(title)

    # Create a new calendar in Google Calendar
    calendar_id = create_calendar(title)

    # add the calendar id to the jars.json file under the new JAR
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['title'] == title:
                jar['calendar_id'] = calendar_id
                break
    
    # write the updated jars.json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

def get_calendar_id_from_database_id(database_id):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == database_id:
                return jar['calendar_id']
            
def get_database_id_from_calendar_id(calendar_id):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['calendar_id'] == calendar_id:
                return jar['database_id']

def get_database_id_from_title(title):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['title'] == title:
                return jar['database_id']
            
def get_calendar_id_from_title(title):  
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['title'] == title:
                return jar['calendar_id']
            
def get_title_from_database_id(database_id):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == database_id:
                return jar['title']
            
def get_title_from_calendar_id(calendar_id):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['calendar_id'] == calendar_id:
                return jar['title']
            

def jar_commit(database_id, title, content, start_time, end_time):
    # Create a new page in Notion
    data = create_page(database_id=database_id, 
                       title=title, 
                       start_time=start_time,
                       end_time=end_time, 
                       content=content)
    
    print(data)

    page_id = data["id"]
    public_url = data["public_url"]

    event_content = f"Public URL: {public_url}\nPage_Id: {page_id}"

    # Create a new event in Google Calendar where content is the public_url
    create_event(title=title,
                    description=event_content,
                    start_time=start_time,
                    end_time=end_time,
                    calendar_id=get_calendar_id_from_database_id(database_id)
                    )
    

if __name__ == '__main__':
    # create_jar("Testing for Ryusei Demo")
    database_id = get_database_id_from_title("Testing for Ryusei Demo")
    jar_commit(database_id=database_id,
               title="Test entry",
               content="This is a test entry",
               start_time="2024-02-17T10:00:00",
               end_time="2024-02-17T12:00:00"
               )