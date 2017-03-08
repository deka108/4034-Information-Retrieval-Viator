from server import config
import json

JSON_FILE_NAME = "%s_facebook.json"

PAGE_MAP = {}

def update_page_map():
    global PAGE_MAP
    PAGE_MAP = {}
    with open(config.RECORDS_DATA_PATH, 'r') as file_handler:
        for line in file_handler.readlines():
            row = [col.strip() for col in line.split(":")]
            page_id = row[0]
            post_count = row[1]
            PAGE_MAP[page_id] = {
                "file_name": JSON_FILE_NAME % page_id,
                "post_count": post_count
            }

update_page_map()

def get_page_ids():
    return PAGE_MAP.keys()


def get_json_file_path(page_id):
    if page_id in PAGE_MAP:
        return config.get_data_path(PAGE_MAP[page_id]["file_name"])


def get_json_filename(page_id):
    if page_id in PAGE_MAP:
        return PAGE_MAP[page_id]["file_name"]


def get_all_json_info():
    return PAGE_MAP


def get_json_data_by_page_id(page_id):
    data_path = get_json_file_path(page_id)
    if data_path:
        with open(data_path, mode='r') as file_handler:
            return json.load(file_handler)


def get_schema_data(file_name=None):
    if not file_name:
        schema_path = config.SCHEMA_DATA_PATH
    else:
        schema_path = config.get_data_path(file_name)

    with open(schema_path, mode='r') as file_handler:
        return json.load(file_handler)
