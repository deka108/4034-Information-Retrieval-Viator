from server import config
import json
import pandas as pd

CSV_FILE_NAME = "{}.csv"
JSON_FILE_NAME = "{}.json"
PAGE_JSON_FILE_NAME = "{}_facebook.json"

RECORDS = {}


def get_page_json_filename(page_id):
    return PAGE_JSON_FILE_NAME.format(page_id)


def get_page_json_filepath(page_id):
    return config.get_data_path(get_page_json_filename(page_id))


def get_json_filename(file_name):
    return JSON_FILE_NAME.format(file_name)


def get_json_filepath(file_name):
    return config.get_data_path(get_json_filename(file_name))


def get_csv_filename(file_name):
    return CSV_FILE_NAME.format(file_name)


def get_csv_filepath(file_name):
    return config.get_data_path(get_csv_filename(file_name))


def init_records():
    global RECORDS
    with open(config.INITIAL_RECORDS_DATA_PATH, 'r', encoding='utf-8') as \
            file_handler:
        RECORDS = json.load(file_handler)


def update_records():
    global RECORDS
    with open(config.RECORDS_DATA_PATH, 'r', encoding='utf-8') as file_handler:
        RECORDS = json.load(file_handler)


def get_json_data_by_page_id(page_id):
    """"Get JSON data by page id"""
    data_path = get_page_json_filepath(page_id)
    if config.check_data_path(data_path):
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
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_page_data_to_json(data, page_id):
    with open(get_page_json_filepath(page_id), mode='w', encoding='utf-8') \
            as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_data_to_json(data, file_name):
    with open(get_json_filepath(file_name), mode='w', encoding='utf-8') \
            as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_dict_to_csv(data, headers, file_name):
    data_path = config.get_data_path(get_csv_filename(file_name))
    df = pd.DataFrame(data)
    df.to_csv(data_path, columns=headers, index=False, index_label="no")


def get_csv_data_by_page_id(page_id):
    return pd.read_csv(get_csv_filepath(page_id))


update_records()


