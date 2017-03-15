from server import config
import json
import pandas as pd

CSV_FILE_NAME = "{}.csv"
JSON_FILE_NAME = "{}.json"
PAGE_JSON_FILE_NAME = "{}_facebook"
PAGE_CSV_FILE_NAME = "{}_facebook"

RECORDS = {}


def get_json_filename(file_name):
    return JSON_FILE_NAME.format(file_name)


def get_page_json_filename(page_id):
    return PAGE_JSON_FILE_NAME.format(page_id)


def get_csv_filename(file_name):
    return CSV_FILE_NAME.format(file_name)


def get_page_csv_filename(page_id):
    return PAGE_CSV_FILE_NAME.format(page_id)


def get_json_filepath(file_name):
    return config.get_data_path(get_json_filename(file_name))


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


def get_preprocessed_json_data_by_page_id(page_id):
    """"Get preprocessed JSON data by page id"""
    df = get_csv_data(get_page_csv_filename(page_id))
    df = df.fillna("")
    return df.to_dict("records")


def get_preprocessed_json_data_all():
    df = get_preprocessed_csv_page_all()
    df = df.fillna("")
    return df.to_dict("records")


def get_raw_json_data_by_page_id(page_id):
    """"Get non preprocessed JSON data by page id"""
    data_path = get_json_filepath(get_page_json_filename(page_id))
    if config.check_data_path(data_path):
        with open(data_path, mode='r') as file_handler:
            return json.load(file_handler)
    else:
        raise FileNotFoundError(
            "Json of the requested page_id: {} does not exist.".format(
                page_id))


def get_csv_data(file_name):
    data_path = get_csv_filepath(file_name)
    if config.check_data_path(data_path):
        df = pd.read_csv(data_path, encoding='utf-8')
        return df
    else:
        raise FileNotFoundError(
            "Csv of the requested page_id: {} does not exist.".format(data_path))


def get_preprocessed_csv_page_all():
    all_pageids = get_page_ids()
    data = []
    for page_id in all_pageids:
        data.append(get_csv_data(get_page_csv_filename(page_id)))
    result = pd.concat(data)
    return result


def get_schema_data(file_name=None):
    if not file_name:
        schema_path = config.SCHEMA_DATA_PATH
    else:
        schema_path = config.get_data_path(file_name)

    with open(schema_path, mode='r') as file_handler:
        return json.load(file_handler)


def get_page_ids():
    """Get page ids"""
    return RECORDS.keys()


def get_records():
    """Get page records with page id maps to count"""
    return RECORDS


def write_records_to_json(data):
    """Update records and write records to json."""

    with open(config.RECORDS_DATA_PATH, mode='w',  encoding='utf-8') as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)
    
    global RECORDS
    RECORDS = data


def write_page_data_to_json(data, page_id):
    with open(get_json_filepath(get_page_json_filename(page_id)), mode='w',
                                encoding='utf-8') as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_data_to_json(data, file_name):
    with open(get_json_filepath(file_name), mode='w', encoding='utf-8') \
            as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_dict_to_csv(data, headers, file_name):
    data_path = config.get_data_path(get_csv_filename(file_name))
    df = pd.DataFrame(data)
    df.to_csv(data_path, columns=headers, index=False, index_label="no",
              encoding='utf-8')

update_records()

