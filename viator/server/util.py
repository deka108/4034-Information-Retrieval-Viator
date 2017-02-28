from server import config
import json

JSON_FILE_NAME = "%s_facebook.json"

DATA_MAP = {}

def update_data_map():
    global DATA_MAP
    DATA_MAP = {}
    with open(config.RECORDS_DATA_PATH, 'r') as file_handler:
        for line in file_handler.readlines():
            page_id = line.split(":")[0]
            DATA_MAP[page_id] = JSON_FILE_NAME % page_id

update_data_map()

def get_data_names():
    return DATA_MAP.keys()

def get_file_path(country):
    if country in DATA_MAP:
        return config.get_data_path(DATA_MAP[country])

def get_file_name(country):
    if country in DATA_MAP:
        return DATA_MAP[country]

def read_json_data(country):
    data_path = get_file_path(country)
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
