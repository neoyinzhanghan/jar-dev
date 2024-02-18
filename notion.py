import os
import requests
import json
from datetime import datetime, timezone

notion_secret = json.load(open("resources/notion_secret.json", "r"))
NOTION_TOKEN = notion_secret["notion_token"]

# import the /Users/neo/Documents/MODS/JAR/jars.json file
jars = json.load(open("/Users/neo/Documents/MODS/JAR/jars.json", "r"))

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_pages(database_id):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    payload = {"page_size": 100}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    results = data["results"]

    with open(f"ledgers/{database_id}.json", 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return results

def get_page(page_id):

    url = f"https://api.notion.com/v1/pages/{page_id}"

    response = requests.get(url, headers=headers)
    data = response.json()

    # with open(f"ledgers/{page_id}.json", 'w', encoding='utf-8') as f:
    #     json.dump(data, f, ensure_ascii=False, indent=4)

    return data

def get_page_info(page_id):

    page = get_page(page_id)

    page_id = page["id"]
    props = page["properties"]
    title = props["Title"]["title"][0]["text"]["content"]
    start_time = props["Start Time"]["date"]["start"]
    end_time = props["End Time"]["date"]["start"]
    public_url = page["public_url"]

    return {
        "id": page_id,
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "public_url": public_url
    }

def get_database_id_from_page_id(page_id):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    response = requests.get(url, headers=headers)
    data = response.json()

    return data["parent"]["database_id"]

def create_database(title='New JAR'):
    # Ensure the directory exists
    if not os.path.exists('ledgers'):
        os.makedirs('ledgers')

    # Your predefined variables like jars and headers need to be defined somewhere above this function
    url = "https://api.notion.com/v1/databases"

    payload = {
        "parent": {"database_id": jars["root_id"]},
        "title": [
            {
                "text": {
                    "content": title
                }
            }
        ],
        "properties": {
            "Title": {
                "title": {}
            },
            "Start Time": {
                "date": {}
            },
            "End Time": {
                "date": {}
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:  # Successful API call
        data = response.json()

        # # Save the database details locally
        # with open(f"ledgers/{data['id']}.json", 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

        # Update the jars dictionary and save changes to jars.json
        jars["jars"].append({
            "title": title,
            "database_id": data["id"],
            "public_url": data["url"]  # Assuming 'url' is the correct key for public_url
        })

        # Write the updated jars to jars.json
        with open('jars.json', 'w', encoding='utf-8') as f:
            json.dump(jars, f, ensure_ascii=False, indent=4)

        return data
    else:
        print(f"Failed to create database: {response.text}")
        return None
    
def delete_page(page_id):

    url = f"https://api.notion.com/v1/pages/{page_id}"

    response = requests.delete(url, headers=headers)
    if response.status_code == 200:  # Successful API call
        data = response.json()
        return data
    else:
        # print(f"Failed to delete page: {response.text}")
        return None
    
def archive_page(page_id):

    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {
        "archived": True
    }

    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:  # Successful API call
        data = response.json()
        return data
    else:
        print(f"Failed to archive page: {response.text}")
        return None
    

    
def create_page(database_id, title, start_time, end_time, content):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Title": {
                "title": [
                    {
                        "text": {
                            "content": title
                        }
                    }
                ]
            },
            "Start Time": {
                "date": {
                    "start": start_time
                }
            },
            "End Time": {
                "date": {
                    "start": end_time
                }
            }
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:  # Successful API call
        new_page_data = response.json()

        # # Save the page details locally
        # with open(f"ledgers/{data['id']}.json", 'w', encoding='utf-8') as f:
        #     json.dump(data, f, ensure_ascii=False, indent=4)

    else:
        print(f"Failed to create page: {response.text}")
        return None
    
    # write the content to the page
    url = f"https://api.notion.com/v1/blocks/{new_page_data['id']}/children"

    payload = {
        "children": [
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": content
                            }
                        }
                    ]
                }
            }
        ]
    }

    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:  # Successful API call
        data = response.json()
        
        return new_page_data
    
    else:
        print(f"Failed to write content to page: {response.text}")
        return None
    

def list_pages(database_id):
    """ Return a list of all page_id in the database """
    pages = get_pages(database_id)

    page_ids = []
    for page in pages:
        page_ids.append(page["id"])

    return page_ids

def change_times(page_id, new_start_time, new_end_time):
    """ Change the start and end times of a page """
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {
        "properties": {
            "Start Time": {
                "date": {
                    "start": new_start_time
                }
            },
            "End Time": {
                "date": {
                    "start": new_end_time
                }
            }
        }
    }

    # Send a PATCH request to the API
    response = requests.patch(url, json=payload, headers=headers)
    if response.status_code == 200:  # Successful API call
        data = response.json()
        return data
    else:
        print(f"Failed to change times: {response.text}")
        return None

if __name__ == "__main__":
    # make sure there is hour minute time in the start_time and end_time
    create_page(database_id="3631f666913542f0bb613f0c591132d2",
                title="Test Page", 
                start_time="2022-07-01T00:00:00",  # Start time at the beginning of July 1st
                end_time="2022-07-02T23:59:00",    # End time just before the end of July 2nd
                content="This is a test page")


    