from server import config
import json

JSON_FILE_NAME = "%s.json"
PAGE_JSON_FILE_NAME = "%s_facebook.json"

RECORDS = {}


def init_records():
    global RECORDS
    with open(config.INITIAL_RECORDS_DATA_PATH, 'r') as file_handler:
        RECORDS = json.load(file_handler)


def update_records():
    global RECORDS
    with open(config.RECORDS_DATA_PATH, 'r') as file_handler:
        RECORDS = json.load(file_handler)


def get_page_json_file_path(page_id):
    return config.get_data_path(get_page_json_filename(page_id))


def get_page_json_filename(page_id):
    return PAGE_JSON_FILE_NAME % page_id


def get_json_filename(file_name):
    return JSON_FILE_NAME % file_name


def get_json_data_by_page_id(page_id):
    """"Get JSON data by page id"""
    data_path = get_page_json_file_path(page_id)
    if config.check_data_path(page_id):
        with open(data_path, mode='r') as file_handler:
            return json.load(file_handler)


def get_schema_data(file_name=None):
    if not file_name:
        schema_path = config.SCHEMA_DATA_PATH
    else:
        schema_path = config.get_data_path(file_name)

    with open(schema_path, mode='r') as file_handler:
        return json.load(file_handler)


def get_page_ids():
    """Read page ids"""
    return RECORDS.keys()


def get_records():
    """Get page records with page id maps to count"""
    return RECORDS


def write_records_to_json(data, file_name=None):
    """Update records and write records to json."""
    if not file_name:
        data_path = config.RECORDS_DATA_PATH
    else:
        data_path = config.get_data_path(get_json_filename(file_name))

    global RECORDS
    RECORDS = data

    with open(data_path, mode='w',  encoding='utf-8') as file_handler:
        json.dump(data, file_handler)


update_records()