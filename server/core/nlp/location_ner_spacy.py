import en_core_web_md
import pandas as pd

from server.utils import data_util as du
from server.utils import text_util as tu

LOC_COLUMNS = ['GPE', 'FACILITY', 'LOC']
OTHER_COLUMNS = ['PRODUCT', 'WORK_OF_ART', 'EVENT']
nlp = en_core_web_md.load()


def _recognise_cols(row, rel_columns, col_name):
    text = row['full_text']
    if not pd.isnull(text):
        doc = nlp(text)
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
            row[col_name] = '$$'.join(contents)

    return row


def recognise_loc(row):
    return _recognise_cols(row, LOC_COLUMNS, "loc")


def recognise_others(row):
    return _recognise_cols(row, OTHER_COLUMNS, "others")


def extract_ner_in_posts(page_id=None):
    if page_id:
        text_data = tu.get_text_data_by_page_id(page_id)
    else:
        text_data = tu.get_text_data_all()
    text_data = text_data.apply(recognise_loc, axis=1)
    text_data = text_data.apply(recognise_others, axis=1)
    print(text_data[['full_text', 'loc_stat', 'loc', 'others', 'others_stat']])

if __name__ == "__main__":
    extract_ner_in_posts()
    # all_page_ids = du.get_page_ids()
    # # extract_ner_in_posts() # too slow!
    #
    # for page_id in all_page_ids:
    #     extract_ner_in_posts(page_id)