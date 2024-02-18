from notion import *
from google_calendar import *
from jar import *

def _event_id_in_clips(event_id, clips):
    for clip in clips:
        if clip["event_id"] == event_id:
            return True
    return False

def _page_id_in_clips(page_id, clips):
    for clip in clips:
        if clip["page_id"] == page_id:
            return True
    return False

def _clip_in_page_ids(clip, page_ids):
    for page_id in page_ids:
        if clip["page_id"] == page_id:
            return True
    return False

def _clip_in_event_ids(clip, event_ids):
    for event_id in event_ids:
        if clip["event_id"] == event_id:
            return True
    return False

def _delete_clip(clip, database_id):
    # read the json file
    with open('jars.json', 'r') as f:
        jars = json.load(f)
        for jar in jars["jars"]:
            if jar['database_id'] == database_id:
                jar["clips"].remove(clip)
                break
    
    # write the json file
    with open('jars.json', 'w', encoding='utf-8') as f:
        json.dump(jars, f, ensure_ascii=False, indent=4)

def sync_clips_additive(database_id):
    calendar_id = get_calendar_id_from_database_id(database_id)
    event_ids = list_events(calendar_id)
    page_ids = list_pages(database_id)
    clips = list_clips_from_database_id(database_id)

    # check if there is any event_ids that are not in the clips
    for event_id in event_ids:
        if not _event_id_in_clips(event_id, clips):
            # create a new clip
            create_clip_from_event_id(event_id)
    
    for page_id in page_ids:
        if not _page_id_in_clips(page_id, clips):
            # create a new clip
            create_clip_from_page_id(page_id)


def sync_clips_subtractive(database_id):
    calendar_id = get_calendar_id_from_database_id(database_id)
    event_ids = list_events(calendar_id)
    page_ids = list_pages(database_id)
    clips = list_clips_from_database_id(database_id)

    for clip in clips:
        # if the clip is not in the page_ids or event_ids, delete it from the json file

        have_event = _clip_in_event_ids(clip, event_ids)
        have_page = _clip_in_page_ids(clip, page_ids)
        if not have_event or not have_page:
            _delete_clip(clip, database_id)

            if have_event:
                calendar_id, event_id = clip["event_id"].split("-----")
                delete_event(calendar_id=calendar_id, event_id=event_id)
            
            if have_page:
                archive_page(clip["page_id"])

def sync_time(clip):
    """ Sync the start and end times of a page and event. """
    event_id = clip["event_id"]
    page_id = clip["page_id"]

    _, start_time, end_time = get_event_info(event_id)
    change_times(page_id, start_time, end_time)

def sync_all_times(database_id):
    """ Sync all times in the database with the calendar. """
    all_clips = list_clips_from_database_id(database_id)
    for clip in all_clips:
        sync_time(clip)

def sync(database_id):
    sync_clips_additive(database_id)
    sync_clips_subtractive(database_id)
    sync_all_times(database_id)

if __name__ == "__main__":
    sync("5d5f91b2-48ff-4656-9cc5-f0508bec0abc")
    sync("3631f666913542f0bb613f0c591132d2")

