from server.utils import data_util
from server.utils import text_util
from pycorenlp import StanfordCoreNLP
import pandas as pd
import ast
import time

from server.utils.data_util import ALL_POSTS_LOCATIONS_FILENAME, \
    PAGE_LOCATION_FILENAME, LOGGING_NER_FILENAME

nlp = StanfordCoreNLP('http://localhost:9000')
NER_COLUMNS = text_util.EXTRACTED_COLUMNS + ['full_text', 'locations']


def run():
    """Extract NER from all posts"""
    extract_location_all()
    update_all_locations()


def run_pageid(page_id):
    """Extract NER from specific page ID"""
    extract_location_page_id(page_id)
    update_all_locations()


def update_all_locations():
    page_ids = data_util.get_page_ids()
    all_locations = []
    for page_id in page_ids:
        try:
            data = get_location_pageid(page_id)
            all_locations.append(data)
        except:
            print("{} does not exist yet in the database".format(
                data_util.PAGE_LOCATION_FILENAME.format(page_id)))
    all_locations = pd.concat(all_locations)
    data_util.write_df_to_csv(all_locations, NER_COLUMNS,
                              ALL_POSTS_LOCATIONS_FILENAME)
    return all_locations


def get_all_locations():
    all_locations = data_util.get_csv_data_from_filename(
        ALL_POSTS_LOCATIONS_FILENAME)
    return all_locations


def get_location_pageid(page_id):
    location_data = data_util.get_csv_data_from_filename(
        data_util.PAGE_LOCATION_FILENAME.format(page_id))
    return location_data


def extract_location_all():
    """Extracting location NER for all pages"""
    print("Recognising locations for all pages...")
    start_time = time.time()
    page_ids = data_util.get_page_ids()
    for page_id in page_ids:
        extract_location_page_id(page_id)
    end_time = time.time()
    elapsed_time = end_time - start_time
    log = "Finished recognising locations for all pages! Elapsed time: {}"\
        .format(elapsed_time)
    print(log)
    data_util.write_text_to_txt(log, LOGGING_NER_FILENAME)


def extract_location_page_id(page_id):
    """Extract Location for current page id"""
    print("Recognising locations for page:{}...".format(page_id))
    start_time = time.time()
    data = data_util.get_csv_data_by_pageid(page_id)
    data['full_text'] = text_util.get_text_data(data)['full_text']
    data['locations'] = data['full_text'].apply(extract_location_from_text)
    end_time = time.time()
    elapsed_time = end_time - start_time
    data_util.write_df_to_csv(data, NER_COLUMNS,
                              PAGE_LOCATION_FILENAME.format(page_id))
    log = "Finish recognising locations for page:{}! Elapsed Time: {}".format(
        page_id, elapsed_time)
    print(log)
    data_util.write_text_to_txt(log, LOGGING_NER_FILENAME)


def extract_location_from_text(text):
    output = nlp.annotate(text, properties={
        'annotators': 'tokenize,ssplit,ner',
        'outputFormat': 'json'
    })

    if type(output) == str:
        output = ast.literal_eval(output)

    # for each sentence in a text / post
    locations = set()
    for sentence in output['sentences']:
        # extract location (combine consecutive ner location)
        prev_loc = False
        location = ""
        for token in sentence['tokens']:
            if token['ner'] == 'LOCATION':
                if prev_loc:
                    location += " " + token['originalText']
                else:
                    location = token['originalText']
                prev_loc = True
            else:
                if prev_loc:
                    locations.add(location)
                    location = ""
                prev_loc = False

        if prev_loc:
            locations.add(location)

    if len(locations) > 0:
        return "$$".join(locations)
    else:
        return ""


if __name__ == "__main__":
    run()