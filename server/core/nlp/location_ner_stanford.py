from server.utils import data_util
from server.utils import text_util
from pycorenlp import StanfordCoreNLP
import pandas as pd
import ast
import time

nlp = StanfordCoreNLP('http://localhost:9000')
NER_COLUMNS = text_util.EXTRACTED_COLUMNS + ['full_text', 'locations']


def run():
    page_ids = data_util.get_page_ids()
    all_posts = pd.DataFrame(columns=NER_COLUMNS)

    start_time = time.time()
    for page_id in page_ids:
        data = data_util.get_csv_data_by_pageid(page_id)
        data['full_text'] = text_util.get_text_data(data)['full_text']
        data['locations'] = data['full_text'].apply(extract_location_from_text)
        data_util.write_df_to_csv(data, NER_COLUMNS, page_id + "_locations")
        all_posts.append(data)
    end_time = time.time()
    print("Elapsed time: ")
    print(end_time - start_time)

    data_util.write_df_to_csv(all_posts, NER_COLUMNS,
                              data_util.ALL_POSTS_LOCATIONS_FILENAME)


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
        return '$$'.join(locations)
    else:
        return ""


if __name__ == "__main__":
    run()