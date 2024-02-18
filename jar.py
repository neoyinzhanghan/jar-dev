import json
import pandas as pd

from notion import *
from google_calendar import *

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
            
def create_clip_from_event_id(event_id):
    """ Get the title, start_time and end_time from the event_id, content is empty string,
    and call jar_commit(database_id, title, content, start_time, end_time). """

    title, start_time, end_time = get_event_info(event_id)
    calendar_id, internal_event_id = event_id.split("-----")

    database_id = get_database_id_from_calendar_id(calendar_id)

    clip = jar_commit(database_id=database_id,
                title=title,
                content="",
                start_time=start_time,
                end_time=end_time
                )
    
    # now delete the event from the calendar
    delete_event(calendar_id, internal_event_id)

    return clip

def create_clip_from_page_id(page_id):
    """ Get the title, start_time, end_time and content from the page_id, and call jar_commit(database_id, title, content, start_time, end_time). """

    page = get_page_info(page_id)
    title = page["title"]
    start_time = page["start_time"]
    end_time = page["end_time"]
    public_url = page["public_url"]

    # if start time is after end time, then print the start time and end time and print title
    if start_time > end_time:
        print(f"Start time: {start_time}")
        print(f"End time: {end_time}")
        print(f"Title: {title}")

        raise ValueError("Start time is after end time")

    database_id = get_database_id_from_page_id(page_id)

    # delete the page from Notion
    archive_page(page_id)

    clip = jar_commit(database_id=database_id,
                title=title,
                content=public_url,
                start_time=start_time,
                end_time=end_time
                )            

    return clip

def jar_commit(database_id, title, content, start_time, end_time):
    # Create a new page in Notion
    data = create_page(database_id=database_id, 
                       title=title, 
                       start_time=start_time,
                       end_time=end_time, 
                       content=content)
    
    # print(data)

    page_id = data["id"]
    public_url = data["public_url"]

    event_content = f"Public URL: {public_url}\nPage_Id: {page_id}"

    # Create a new event in Google Calendar where content is the public_url
    event_data = create_event(title=title,
                    description=event_content,
                    start_time=start_time,
                    end_time=end_time,
                    calendar_id=get_calendar_id_from_database_id(database_id)
                    )
    
    event_id = get_calendar_id_from_database_id(database_id)+'-----'+event_data["id"]

    clip = {"page_id": page_id, 
            "page_public_url": public_url, 
            "event_id": event_id}
    
    # write the clip to the jars.json file jars["jars"][i]["clips"] which is a list
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == database_id:
                jar['clips'].append(clip)
                break
    
    # write the updated jars.json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

    return clip
    
def list_clips_from_database_id(database_id):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == database_id:
                return jar['clips']
            
def list_clips_from_calendar_id(calendar_id):
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['calendar_id'] == calendar_id:
                return jar['clips']

def delete_clip_using_page_id(page_id):
    """ Delete a clip from the database using the page_id. """

    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == get_database_id_from_page_id(page_id):
                for clip in jar['clips']:
                    if clip['page_id'] == page_id:
                        jar['clips'].remove(clip)

                        page_id_to_delete = page_id
                        event_id_to_delete = clip['event_id']

                        archive_page(page_id_to_delete)
                        delete_event(event_id_to_delete.split("-----")[0], event_id_to_delete.split("-----")[1])

                        break
                break
        
        # write the updated jars.json file
        with open('jars.json', 'w', encoding='utf-8') as f:
            json.dump(jars, f, ensure_ascii=False, indent=4)       
    
    # write the updated jars.json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

def edit_jar_title(database_id, new_title):
    """ Edit the title of the JAR with database_id to new_title. """

    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == database_id:

                old_title = jar['title']

                if old_title == new_title:
                    return None
                else:
                    jar['title'] = new_title
                    break
    
    # write the updated jars.json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

    # now change the title in the notion database and calendar event
    edit_database_title(database_id, new_title)
    edit_calendar_title(get_calendar_id_from_database_id(database_id), new_title)

def edit_clip_title(page_id, new_title):
    """ Edit the title of the clip with page_id to new_title. """

    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            for clip in jar['clips']:
                if clip['page_id'] == page_id:
                    event_id = clip['event_id']

        old_title = get_page_info(page_id)["title"]
        if old_title != new_title:
            edit_page_title(page_id, new_title)
            edit_event_title(event_id.split("-----")[0],event_id.split("-----")[1],  new_title)

                    
    
    # write the updated jars.json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

    # now change the title in the notion database and calendar event
    edit_page_title(page_id, new_title)
    edit_event_title(get_calendar_id_from_database_id(get_database_id_from_page_id(page_id)), new_title)

def edit_clip_content(page_id, new_content):
    """ Edit the content of the clip with page_id to new_content. """

    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            for clip in jar['clips']:
                if clip['page_id'] == page_id:
                    event_id = clip['event_id']

        old_content = get_page_content(page_id)
        if old_content != new_content:
            edit_page_content(page_id, new_content)

    # write the updated jars.json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

    # now change the content in the notion database and calendar event
    edit_page_content(page_id, new_content)

def get_jars_dct_title_key():
    """ Return a dictionary of all the JARs with their database_id, calendar_id and public_url.
    The dictionary keys are the jar titles, if there is title duplicate just add an index to the title.
    """

    with open('jars.json', 'r') as f:
        jars = json.load(f)
        jars_dct = {}
        for jar in jars["jars"]:
            title = jar['title']

            if title in jars_dct:
                i = 1
                while title+str(i) in jars_dct:
                    i += 1
                title += str(i)

            database_id = jar['database_id']
            calendar_id = jar['calendar_id']
            public_url = jar['public_url']
            jars_dct[title] = {"database_id": database_id, "calendar_id": calendar_id, "public_url": public_url}

        return jars_dct

def get_jar_ledger_as_pd(database_id):
    """ Return a pandas dataframe of all the clips in the JAR with database_id. """

    clips = list_clips_from_database_id(database_id)

    df_dct = {"Title": [], "Start Time": [], "End Time": [], "Public URL": [], "Content": [], "Page Id": [], "Event Id": []}

    for clip in clips:
        page_id = clip["page_id"]
        page = get_page_info(page_id)
        content = get_page_content(page_id)
        df_dct["Title"].append(page["title"])
        df_dct["Start Time"].append(page["start_time"])
        df_dct["End Time"].append(page["end_time"])
        df_dct["Public URL"].append(page["public_url"])
        df_dct["Content"].append(content)
        df_dct["Page Id"].append(page_id)
        df_dct["Event Id"].append(clip["event_id"])

    df = pd.DataFrame(df_dct)



    return df

if __name__ == '__main__':
    # create_jar("Testing for Ryusei Demo")
    database_id = get_database_id_from_title("Testing for Ryusei Demo")
    print(get_jar_ledger_as_pd(database_id))