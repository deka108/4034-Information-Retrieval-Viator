from server.utils import text_util as tu
from server.utils import data_util as du
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer
import nltk


lemmatizer = WordNetLemmatizer()


# per sentence
def extract_noun_and_verb(text):
    noun_verbs = []
    pos_tags = extract_pos_tag_from_post(text)
    for sentence in pos_tags:
        noun_verbs_sent = set()
        for token in sentence:
            word = lemmatizer.lemmatize(tu.clean_text(token[0]))
            if len(word) > 2 and word not in tu.stop_words:
                if token[1] == 'NN' or token[1] == 'NNS' or token[1].startswith(
                        'VB'):
                    noun_verbs_sent.add(word)
        if noun_verbs_sent:
            noun_verbs_sent = list(noun_verbs_sent)
            noun_verbs_sent.sort()
            noun_verbs.append(noun_verbs_sent)
    return noun_verbs


def extract_pronoun():
    all_posts = extract_nouns_verbs_from_posts()
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


def extract_nouns_verbs_from_posts():
    page_ids = du.get_page_ids()
    all_results = []
    for page_id in page_ids:
        # word-sentences per post id
        res = extract_nouns_verbs_by_pageid(page_id)
        # concat word-sentences for all post id
        if res:
            all_results += res
    return all_results


def extract_nouns_verbs_by_pageid(page_id):
    text_data = tu.get_text_data_by_page_id(page_id)
    all_results = []
    for idx, row in text_data.iterrows():
        res = extract_noun_and_verb(row['full_text'])
        # concat all results
        all_results += res
    return all_results


if __name__ == "__main__":
    # extract_pronoun()
    print(extract_nouns_verbs_from_posts())