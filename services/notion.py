from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))

DATA_SOURCE_ID = "4b47dd3e-dfbd-49fc-a767-3b951ebd4e0b"

def get_tasks():
    response = notion.data_sources.query(
        data_source_id=DATA_SOURCE_ID
    )

    tasks = []

    for page in response["results"]:
        props = page["properties"]

        task_name = props["Task"]["title"][0]["plain_text"] if props["Task"]["title"] else ""

        tasks.append({
            "Task": task_name,
            "Priority": props["Priority"]["select"]["name"] if props["Priority"]["select"] else "",
            "Status": props["Status"]["select"]["name"] if props["Status"]["select"] else "",
            "Category": props["Category"]["select"]["name"] if props["Category"]["select"] else "",
            "Hours": props["Estimated Hours"]["number"],
        })

    return tasks