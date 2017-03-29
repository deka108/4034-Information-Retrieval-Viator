from server.utils import text_util as tu
from server.utils import data_util as du
from textblob import TextBlob
import os
import json


def extract_pronoun():
    all_posts = extract_pos_tag_from_posts()
    pronouns = set()
    pronoun = ""
    prev_nnp = False
    for post in all_posts:
        for token in post:
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
    sentences = TextBlob(text)

    return sentences.tags


def extract_pos_tag_from_posts():
    # text_data = tu.get_text_data_all()
    # tagged_posts = text_data['full_text'].apply(get_pronoun)

    page_ids = du.get_page_ids()
    for page_id in page_ids:
        text_data = tu.get_text_data_by_page_id(page_id)
        print(text_data['full_text'])
        break
        # tagged_posts = text_data['full_text'].apply(extract_pos_tag_from_post)
        # with open("post_tag.text", "w") as fh:
        #     for post in tagged_posts:
        #         fh.write(post)
        #         fh.write("\n")
        # print(tagged_posts)
        # break

    # tagged_posts.to_pickle("post_tag.pickle")
    # return tagged_posts


if __name__ == "__main__":
    # extract_pronoun()
    extract_pos_tag_from_posts()