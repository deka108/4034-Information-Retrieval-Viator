from gensim import corpora, models
from server.utils import data_util as du
from server.utils import text_util as tu

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


def generate_topic():
    dictionary, corpus = load_dict_corpus()
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=5)
    lsi.print_topic(topicno=1)


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
    data = data['full_text'].apply(tu.preprocess_text)
    return data.tolist()

if __name__ == "__main__":
    texts = preprocess_post()
    print(texts)
    gensim_pipeline(texts)
    generate_topic()