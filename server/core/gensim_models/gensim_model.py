import logging

import numpy as np
import pandas as pd
from gensim import corpora, models

from server.core.nlp import postags_nltk
from server.core.topic_classification import classification_preprocessing as cp

from server.utils import data_util as du
from server.utils import text_util as tu

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s',
                    level=logging.INFO)

USE_LABEL_DATA = False
SUFFIX = ""

if USE_LABEL_DATA:
    SUFFIX = "-label"
else:
    SUFFIX = "-all"

NUM_FEATURES = 300
DOCUMENT_MAX_NUM_WORDS = 100
CONTEXT = 10


freq = {}


def load_dict_corpus():
    try:
        dictionary = corpora.Dictionary.load(du.get_gensim_dict_path(SUFFIX))
        corpus = corpora.MmCorpus(du.get_gensim_corpus_path(SUFFIX))
        return dictionary, corpus
    except:
        print("Corpus does not exist")


def load_tfidf_model():
    try:
        tfidf_model = models.TfidfModel.load(du.get_gensim_tfidf_path(SUFFIX))
        return tfidf_model
    except:
        print("Tfidf model does not exist")


def load_lsi_model():
    try:
        lsi_model = models.LsiModel.load(du.get_gensim_lsi_path(SUFFIX))
        return lsi_model
    except:
        print("LSI model does not exist")


def load_lda_model():
    try:
        lda_model = models.LdaModel.load(du.get_gensim_lda_path(SUFFIX))
        return lda_model
    except:
        print("LDA model does not exist")


def load_w2v_model():
    try:
        w2v_model = models.Word2Vec.load(du.get_gensim_w2v_path(SUFFIX))
        return w2v_model
    except:
        print("W2V model does not exist")


def load_d2v_model():
    try:
        d2v_model = models.Doc2Vec.load(du.get_gensim_d2v_path(SUFFIX))
        return d2v_model
    except:
        print("D2V model does not exist")


def generate_word2vec_model(sentences):
    model_word2vec = models.Word2Vec(sentences, size=NUM_FEATURES, window=10)
    model_word2vec.init_sims(True)
    model_word2vec.save(du.get_filepath(du.get_gensim_w2v_path(SUFFIX)))
    return model_word2vec


def generate_doc2vec_model(docs):
    model_doc2vec = models.Doc2Vec(docs, size=NUM_FEATURES)
    model_doc2vec.init_sims(True)
    model_doc2vec.save(du.get_filepath(du.get_gensim_d2v_path(SUFFIX)))
    return model_doc2vec


def generate_tfidf_model():
    dictionary, corpus = load_dict_corpus()
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    tfidf.save(du.get_filepath(du.get_gensim_tfidf_path(SUFFIX)))
    return corpus_tfidf


def generate_topic_lsi():
    dictionary, corpus = load_dict_corpus()
    corpus_tfidf = generate_tfidf_model()
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary,
                          num_topics=NUM_FEATURES)
    lsi.save(du.get_filepath(du.get_gensim_lsi_path(SUFFIX)))
    return lsi


def generate_topic_lda():
    dictionary, corpus = load_dict_corpus()
    lda = models.LdaModel(corpus, num_topics=NUM_FEATURES)
    lda.save(du.get_filepath(du.get_gensim_lda_path(SUFFIX)))
    return lda


def gensim_pipeline(texts):
    dictionary = corpora.Dictionary(texts)
    dictionary.save(du.get_gensim_dict_path(SUFFIX))
    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize(du.get_filepath(du.get_gensim_corpus_path(
        SUFFIX)), corpus)


def generate_w2v_features(docs, labels=None, num_of_categories=5):
    w2v_model = load_w2v_model()
    num_of_docs = len(docs)

    X = np.zeros(shape=(num_of_docs, DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES)).\
        astype(np.float32)
    Y = np.zeros(shape=(num_of_docs,
                        num_of_categories)).astype(np.float32)
    empty_word = np.zeros(NUM_FEATURES).astype(np.float32)

    DOC_MIN_WORDS = 1000000
    DOC_MAX_WORDS = 0

    for idx, document in enumerate(docs):
        # for jdx, word in enumerate(document):
        #     if jdx == DOCUMENT_MAX_NUM_WORDS:
        #         break
        #     else:
        #         if word in w2v_model:
        #             X[idx, jdx, :] = w2v_model[word]
        #         else:
        #             X[idx, jdx, :] = empty_word
        jdx = 0
        for word in document:
            if jdx < DOCUMENT_MAX_NUM_WORDS:
                if word in w2v_model:
                    X[idx, jdx, :] = w2v_model[word]
                    jdx += 1

        DOC_MIN_WORDS = min(jdx, DOC_MIN_WORDS)
        DOC_MAX_WORDS = max(jdx, DOC_MAX_WORDS)
        # jdx = 0
        # for word in document:
        #     if word in w2v_model:
        #        jdx += 1
    print("Max words: {}".format(DOC_MAX_WORDS))
    print("Min words: {}".format(DOC_MIN_WORDS))
    if not labels.empty:
        Y = pd.get_dummies(labels).as_matrix()

    return X, Y


def generate_d2v_features(docs, labels=None, num_of_categories=5):
    d2v_model = load_d2v_model()
    num_of_docs = len(docs)

    X = np.zeros(shape=(num_of_docs, DOCUMENT_MAX_NUM_WORDS, NUM_FEATURES)).\
        astype(np.float32)
    Y = np.zeros(shape=(num_of_docs,
                        num_of_categories)).astype(np.float32)
    empty_word = np.zeros(NUM_FEATURES).astype(np.float32)
    print()
    print(d2v_model[docs[0][0]])
    # for idx, document in enumerate(docs):
    #     for jdx, word in enumerate(document):
    #         if jdx == DOCUMENT_MAX_NUM_WORDS:
    #             break
    #         else:
    #             if word in d2v_model:
    #                 X[idx, jdx, :] = d2v_model[word]
    #             else:
    #                 X[idx, jdx, :] = empty_word

    if not labels.empty:
        Y = pd.get_dummies(labels).as_matrix()

    return X, Y


def get_noun_verbs(page_id=None):
    if page_id:
        noun_verbs = postags_nltk.extract_nouns_verbs_by_pageid(page_id)
    else:
        noun_verbs = postags_nltk.extract_nouns_verbs_from_posts()
    return noun_verbs


def get_data():
    if USE_LABEL_DATA:
        X = cp.get_all_data()[0]
    else:
        X = tu.get_text_data_all()
        X = X['full_text']
    return X


def generate_features(opt=None):
    global USE_LABEL_DATA
    USE_LABEL_DATA = True

    texts = cp.get_posts()
    labels = cp.get_labels()
    if not opt or opt == "w2v":
        return generate_w2v_features(texts, labels)


if __name__ == "__main__":
    # pass
    texts = cp.get_posts()
    labels = cp.get_labels()

    gensim_pipeline(texts)
    generate_tfidf_model()
    generate_topic_lsi()
    generate_topic_lda()

    generate_word2vec_model(texts)
    docs = cp.get_cleaned_docs()
    generate_doc2vec_model(docs)

    # generate_w2v_features(texts, labels)