from server.utils import text_util as tu
from server.utils import data_util as du
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
import nltk
import os
import json


def extract_pronoun():
    all_posts = extract_pos_tag_from_posts()
    pronouns = set()
    pronoun = ""
    prev_nnp = False
    for post in all_posts:
        for sentence in post:
            for token in sentence:
                if token[1] == 'NNP':
                    if prev_nnp:
                        pronoun += " " + token[0]
                    else:
                        pronoun = token[0]
                    prev_nnp = True
                else:
                    if prev_nnp:
                        pronouns.add(pronoun)
                    prev_nnp = False
                    pronoun = ""
    if prev_nnp:
        pronouns.add(pronoun)
    pronouns = list(pronouns)
    pronouns.sort()
    print(pronouns)


def extract_pos_tag_from_post(text):
    sentences = sent_tokenize(text)
    sentences = [word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = nltk.pos_tag_sents(sentences)

    return tagged_sentences


def extract_pos_tag_from_posts():
    # text_data = tu.get_text_data_all()
    # tagged_posts = text_data['full_text'].apply(get_pronoun)

    page_ids = du.get_page_ids()
    for page_id in page_ids:
        text_data = tu.get_text_data_by_page_id(page_id)
        tagged_posts = text_data['full_text'].apply(extract_pos_tag_from_post)
        json_obj = tagged_posts.to_json()
        with open("post_tag.json", "w") as fh:
            json.dump(json_obj, fh, sort_keys=True)
        print(tagged_posts)
        break

    # tagged_posts.to_pickle("post_tag.pickle")
    return tagged_posts


if __name__ == "__main__":
    extract_pronoun()