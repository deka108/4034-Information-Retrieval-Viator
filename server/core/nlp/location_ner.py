import spacy
import pandas as pd
import en_core_web_md

from server.utils import data_util as du

LOC_COLUMNS = ['GPE', 'FACILITY', 'LOC']
OTHER_COLUMNS = ['PRODUCT', 'WORK_OF_ART', 'EVENT']
nlp = en_core_web_md.load()


def _recognise_cols(row, rel_columns, col_name):
    msg = row['message']
    if not pd.isnull(msg):
        doc = nlp(msg)
        ents = {}
        contents = []

        for ent in doc.ents:

            if ent.label_ in rel_columns:
                if ent.label_ not in ents:
                    ents[ent.label_] = {}

                ents_label = ents[ent.label_]

                if ent.text in ents_label:
                    ents_label[ent.text] += 1
                else:
                    ents_label[ent.text] = 1
                    contents.append(ent.text)

        if len(ents) != 0:
            row[col_name + "_stat"] = ents
            row[col_name] = ','.join(contents)

    return row


def get_text(row):
    name = row["name"]
    caption = row["caption"]
    message = row["message"]
    row['full_text'] = "{} {} {}".format(name if pd.notnull(name) else "",
                             caption if pd.notnull(caption) else "",
                             message if pd.notnull(message) else "")
    return row


def recognise_loc(row):
    return _recognise_cols(row, LOC_COLUMNS, "loc")


def recognise_others(row):
    return _recognise_cols(row, OTHER_COLUMNS, "others")


def extract_ner_in_posts(page_id):
    data = du.get_csv_data_by_pageid(page_id)
    data = data.apply(get_text, axis=1)
    data = data.apply(recognise_loc, axis=1)
    data = data.apply(recognise_others, axis=1)
    print(data[['full_text', 'loc_stat', 'loc', 'others', 'others_stat']])


if __name__ == "__main__":
    all_page_ids = du.get_page_ids()
    for page_id in all_page_ids:
        extract_ner_in_posts(page_id)