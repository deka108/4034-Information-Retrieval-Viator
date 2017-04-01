from gensim import corpora, models
from server.utils import data_util as du
from server.utils import text_util as tu
from server.core.nlp import postags_spacy, postags_nltk

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

DICT_PATH = "tmp/post.dict"
CORPUS_PATH = "tmp/post.mm"

DICT_PATH_PAGEID = "tmp/post-{}.dict"
CORPUS_PATH_PAGEID = "tmp/post-{}.mm"


def load_dict_corpus():
    try:
        dictionary = corpora.Dictionary.load(DICT_PATH)
        corpus = corpora.MmCorpus(CORPUS_PATH)
        return dictionary, corpus
    except:
        print("Corpus does not exist")


def generate_topic_lsi():
    dictionary, corpus = load_dict_corpus()
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
    lsi.print_topics()


def generate_topic_lda():
    dictionary, corpus = load_dict_corpus()
    lda = models.LdaModel(corpus, id2words=dictionary, num_topics=5)
    lda.print_topics()


def gensim_pipeline(texts):
    dictionary = corpora.Dictionary(texts)
    dictionary.save(DICT_PATH)
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(CORPUS_PATH, corpus)


def preprocess_post(page_id=None):
    if page_id:
        data = tu.get_text_data_by_page_id(page_id)
    else:
        data = tu.get_text_data_all()
    data = data['full_text'].apply(lambda row: tu.preprocess_text(row,
                                                                  stem=True,
                                                                  lemmatize=False))
    return data.tolist()


def get_noun_verbs(page_id=None):
    if page_id:
        noun_verbs = postags_nltk.extract_nouns_verbs_by_pageid(page_id)
    else:
        noun_verbs = postags_nltk.extract_nouns_verbs_from_posts()
    return noun_verbs


if __name__ == "__main__":
    texts = get_noun_verbs()
    gensim_pipeline(texts)
    generate_topic_lsi()