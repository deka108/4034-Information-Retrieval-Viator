from server import config
import json
import pandas as pd

CSV_FILENAME = "{}.csv"
JSON_FILENAME = "{}.json"
TXT_FILENAME = "{}.txt"
PAGE_JSON_FILENAME = "{}_facebook"
PAGE_CSV_FILENAME = "{}_facebook"
ALL_POSTS_FILENAME = "all_posts"
ALL_POSTS_LOCATIONS_FILENAME = "all_posts_with_locations"
ALL_POSTS_COMMENTS_FILENAME = "all_posts_with_comments"
ALL_LOCATION_CORPUS_FILENAME = "location_corpus_all"
PAGE_LOCATION_FILENAME = "{}_locations"
ORDERED_DATA_FILENAME = "ordered_data"
SHUFFLED_DATA_FILENAME = "shuffled_data"
TOPIC_LABELLED_FILENAME = "topic_labelled"
LOGGING_NER_FILENAME = "logging_ner"
LOGGING_TOPIC_FILENAME = "logging_topic"
LOGGING_SENTIMENT_FILENAME = "logging_sentiment"
SPLITTED_DATA_FILENAME = "splitted_data_{}"
NEW_LOCATION_CORPUS_FILENAME = "new_location_corpus"
NEW_LOCATION_CORPUS_ALL_FILENAME = "new_location_corpus_all"
SPLIT_LOCATION_CORPUS_FILENAME = "new_location_corpus_{}"

TESTING = "testing"

RECORDS_DB = {}
RECORDS_SOLR = {}


def get_json_filename(file_name):
    return JSON_FILENAME.format(file_name)


def get_page_json_filename(page_id):
    return PAGE_JSON_FILENAME.format(page_id)


def get_csv_filename(file_name):
    return CSV_FILENAME.format(file_name)


def get_txt_filename(file_name):
    return TXT_FILENAME.format(file_name)


def get_page_csv_filename(page_id):
    return PAGE_CSV_FILENAME.format(page_id)


def get_json_filepath(file_name):
    return config.get_data_path(get_json_filename(file_name))


def get_csv_filepath(file_name):
    return config.get_data_path(get_csv_filename(file_name))


def get_splitted_csv_filepath(id):
    return config.get_splitted_data_path(get_csv_filename(
        SPLITTED_DATA_FILENAME.format(id)))


def get_labelled_csv_filepath(id):
    return config.get_labelled_data_path(get_csv_filename(
        SPLITTED_DATA_FILENAME.format(id)))


def init_db_records():
    global RECORDS_DB
    with open(config.INITIAL_RECORDS_DATA_PATH, 'r', encoding='utf-8') as \
            file_handler:
        RECORDS_DB = json.load(file_handler)


def update_db_records():
    global RECORDS_DB
    with open(config.DB_RECORDS_DATA_PATH, 'r', encoding='utf-8') as file_handler:
        RECORDS_DB = json.load(file_handler)


def update_solr_records():
    global RECORDS_SOLR
    with open(config.SOLR_RECORDS_DATA_PATH, 'r', encoding='utf-8') as file_handler:
        RECORDS_SOLR = json.load(file_handler)

update_db_records()
update_solr_records()


def get_preprocessed_json_data_by_page_id(page_id):
    """"Get preprocessed JSON data by page id"""
    return get_json_data_from_csv(get_csv_filepath(get_page_csv_filename(page_id)))


def get_json_data_from_csv(csv_path):
    df = get_csv_data_from_path(csv_path)
    df = df.fillna("")
    return df.to_dict("records")


def get_preprocessed_json_data_all():
    df = get_all_posts()
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


def get_csv_data_from_filename(file_name):
    return get_csv_data_from_path(get_csv_filepath(file_name))


def get_csv_data_from_path(data_path):
    if config.check_data_path(data_path):
        df = pd.read_csv(data_path, encoding='utf-8')
        df.fillna("")
        return df
    else:
        raise FileNotFoundError(
            "Csv of the requested page_id: {} does not exist.".format(data_path))


def get_csv_data_by_pageid(page_id):
    data_path = get_csv_filepath(get_page_csv_filename(page_id))
    return get_csv_data_from_path(data_path)


def get_csv_data_all():
    all_pageids = get_page_ids()
    data = []
    for page_id in all_pageids:
        data.append(get_csv_data_by_pageid(page_id))
    result = pd.concat(data)
    return result


def get_all_posts():
    return get_csv_data_from_filename(ALL_POSTS_FILENAME)


def get_all_posts_with_comments():
    # return get_df_from_pickle(ALL_POSTS_COMMENTS_FILENAME)
    return get_csv_data_from_filename(ALL_POSTS_COMMENTS_FILENAME)


def get_schema_data(file_name=None):
    if not file_name:
        schema_path = config.SCHEMA_DATA_PATH
    else:
        schema_path = config.get_data_path(file_name)

    with open(schema_path, mode='r') as file_handler:
        return json.load(file_handler)


def get_page_ids():
    """Get page ids"""
    return RECORDS_DB.keys()


def get_db_records():
    """Get page records with page id maps to count"""
    return RECORDS_DB


def get_solr_records():
    """Get page records with page id maps to count"""
    return RECORDS_SOLR


def write_db_records_to_json(data):
    """Update records and write records to json."""

    with open(config.DB_RECORDS_DATA_PATH, mode='w', encoding='utf-8') as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)
    
    global RECORDS_DB
    RECORDS_DB = data


def write_solr_records_to_json(data):
    """Update records and write time records to json."""

    with open(config.SOLR_RECORDS_DATA_PATH, mode='w', encoding='utf-8') as \
            file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)

    global RECORDS_SOLR
    RECORDS_SOLR = data


def write_page_data_to_json(data, page_id):
    with open(get_json_filepath(get_page_json_filename(page_id)), mode='w',
                                encoding='utf-8') as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_data_to_json(data, file_name):
    with open(get_json_filepath(file_name), mode='w', encoding='utf-8') \
            as file_handler:
        json.dump(data, file_handler, indent=2, sort_keys=True)


def write_dict_to_csv(data, headers, file_name):
    df = pd.DataFrame(data)
    write_df_to_csv(df, headers, file_name)


def write_df_to_csv(df, headers, file_name):
    data_path = config.get_data_path(get_csv_filename(file_name))
    df = df.fillna("")
    df.to_csv(data_path, columns=headers, index=False, encoding='utf-8')


def write_df_to_existing_csv(new_df, headers, file_name):
    data_path = config.get_data_path(get_csv_filename(file_name))
    df_csv = pd.read_csv(data_path)
    print(new_df)
    df_csv[headers] = new_df[headers]

    df_csv.to_csv(data_path, columns = df_csv.columns, index=False, encoding='utf-8')
    # write_df_to_csv(df_csv, df_csv.columns, file_name)


def write_text_to_txt(text, file_name, write_mode="a"):
    data_path = config.get_data_path(get_txt_filename(file_name))

    with open(data_path, mode=write_mode, encoding="utf-8") as file_handler:
        file_handler.write(text)
        file_handler.write("\n\n")