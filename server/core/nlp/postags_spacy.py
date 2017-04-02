from server.utils import text_util as tu
from server.utils import data_util as du
import spacy

nlp = spacy.load("en")


def extract_pos_tag_from_post(text):
    doc = nlp(text)
    verbs_nouns = set()
    for word in doc:
        token = word.lemma_
        token = tu.clean_text(token)
        if len(token) > 2 and token not in tu.stop_words:
            if word.pos_ == "VERB" or word.pos_ == "NOUN":
                verbs_nouns.add(token)
    return list(verbs_nouns)


def extract_nouns_verbs_from_posts():
    page_ids = du.get_page_ids()
    all_words = []
    for page_id in page_ids:
        res = extract_nouns_verbs_by_pageid(page_id)
        all_words += res
    return all_words


def extract_nouns_verbs_by_pageid(page_id):
    text_data = tu.get_text_data_by_page_id(page_id)
    all_words = []
    for idx, row in text_data.iterrows():
        res = extract_pos_tag_from_post(row['full_text'])
        # per post
        if res:
            all_words.append(res)
    return all_words


if __name__ == "__main__":
    print(extract_nouns_verbs_from_posts())