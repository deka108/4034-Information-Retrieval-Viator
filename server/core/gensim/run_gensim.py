from gensim import corpora, models
from gensim.models import doc2vec

from server.core.topic_classification import classification_preprocessing as cp
from server.utils import text_util as tu
from server.core.nlp import postags_nltk

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

DICT_PATH = "tmp/post.dict"
CORPUS_PATH = "tmp/post.mm"
TFIDF_PATH = "tmp/model.tfidf"
WORD2VEC_PATH = "tmp/model.word2vec"
DOC2VEC_PATH = "tmp/model.doc2vec"
LDA_PATH = "tmp/model.lda"
LSI_PATH = "tmp/model.lsi"

DICT_PATH_PAGEID = "tmp/post-{}.dict"
CORPUS_PATH_PAGEID = "tmp/post-{}.mm"
freq = {}


def load_dict_corpus():
    try:
        dictionary = corpora.Dictionary.load(DICT_PATH)
        corpus = corpora.MmCorpus(CORPUS_PATH)
        return dictionary, corpus
    except:
        print("Corpus does not exist")


def load_tfidf_model():
    try:
        tfidf_model = models.TfidfModel.load(TFIDF_PATH)
        return tfidf_model
    except:
        print("Tfidf model does not exist")


def load_lsi_model():
    try:
        lsi_model = models.LsiModel.load(LSI_PATH)
        return lsi_model
    except:
        print("LSI model does not exist")


def load_lda_model():
    try:
        lda_model = models.LdaModel.load(LDA_PATH)
        return lda_model
    except:
        print("LDA model does not exist")


def generate_word2vec_model(sentences):
    model_word2vec = models.Word2Vec(sentences, size=300, window=10)
    return model_word2vec


def generate_doc2vec_model(docs):
    model_doc2vec = models.Doc2Vec(docs, size=300)
    return model_doc2vec


def generate_tfidf_model():
    dictionary, corpus = load_dict_corpus()
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    tfidf.save(TFIDF_PATH)
    return corpus_tfidf


def generate_topic_lsi():
    dictionary, corpus = load_dict_corpus()
    corpus_tfidf = generate_tfidf_model()
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=300)
    lsi.save(LSI_PATH)
    # lsi.print_topics()
    return lsi


def generate_topic_lda():
    dictionary, corpus = load_dict_corpus()
    lda = models.LdaModel(corpus, num_topics=300)
    lda.save(LDA_PATH)
    # lda.print_topics()
    return lda


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


def get_sentences():
    X = tu.get_text_data_all()
    X = X['full_text']
    sentences = cp.preprocess(X)
    for sentence in sentences:
        for token in sentence:
            if token in freq:
                freq[token] += 1
            else:
                freq[token] = 1
    sentences = [[token for token in sentence if freq[token] > 1] for
                 sentence in sentences]
    return sentences


def get_docs():
    X = tu.get_text_data_all()
    X = X['full_text']
    return cp.preprocess_docs(X)


if __name__ == "__main__":
    # texts = get_sentences()
    # gensim_pipeline(texts)
    # generate_tfidf_model()
    # generate_topic_lsi()
    # generate_topic_lda()
    # generate_word2vec_model(texts)

    docs = get_docs()
    generate_doc2vec_model(docs)