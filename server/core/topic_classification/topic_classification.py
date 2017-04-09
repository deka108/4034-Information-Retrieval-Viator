from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score
from sklearn.externals import joblib
from server.core.topic_classification import classification_preprocessing as cp
from server.core.topic_classification.classifier import VClassifier
from server.utils import data_util as du
from server import config
import pandas as pd
import numpy as np
import nltk
import time
import pickle
from server.utils.data_util import LOGGING_TOPIC_FILENAME


#1. Food
#2. Event
#3. Nature
#4. Accommodation
#5. Attraction

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


def add_topic(page_id):
    global shape
    """TESTING"""
    print("Recognising topics for page:{}...".format(page_id))
    start_time = time.time()
    vocab = joblib.load(du.get_filepath(du.VOCAB_PICKLE_FILENAME))
    model = VClassifier()

    test_df = du.get_csv_data_by_pageid(page_id)

    test = test_df.loc[test_df["page_id"] == page_id]
    headers = test.columns.tolist()
    if 'predicted_class' in headers:
        headers.remove('predicted_class')
    test = test.loc[:, headers]
    test_data = test.loc[:, ["id", "page_id", "message", "description"]]
    test_id = test_data.loc[:, ["id"]]
    test_msg = test_data.loc[:, ["message"]]
    test_msg = test_msg.replace(np.nan, '', regex=True)
    test_msg = list(test_msg.values.flatten())
    test_desc = test_data.loc[:, ["description"]]
    test_desc = test_desc.replace(np.nan, '', regex=True)
    test_desc = list(test_desc.values.flatten())

    test_post = list()

    for i in range(len(test_msg)):
        temp = test_msg[i] + test_desc[i]
        test_post.append(temp)

    vectorizer = CountVectorizer(min_df=1, vocabulary=vocab,
                                 tokenizer=LemmaTokenizer())
    test_count = vectorizer.fit_transform(test_post)

    test_transformer = TfidfTransformer(use_idf=True).fit(test_count)
    test_tf = test_transformer.transform(test_count)

    test_result = model.predict(test_tf)

    test_result = list(map(float, test_result))
    test_result = list(map(int, test_result))

    id_result = np.column_stack((test_id, test_result))
    end_time = time.time()
    elapsed_time = end_time - start_time
    shape = test_tf.shape[0]
    speed = shape/elapsed_time

    log = "Finish recognising topics for page:{}! Elapsed Time: {}\n".format(
        page_id, elapsed_time)
    log += "Classification speed, samples per second = " + str(speed)
    print(log)

    result_df = pd.DataFrame(id_result, columns = ["id", "predicted_class"])


    predicted = test.merge(result_df, on=["id"])

    filename = page_id + "_facebook.csv"
    filepath = config.get_data_path(filename)
    predicted.to_csv(filepath, encoding='utf-8')
    du.write_text_to_txt(log, LOGGING_TOPIC_FILENAME)
    print("Predicted class saved to " + filename)


def add_topic_to_all_pages():
    page_ids = du.get_page_ids()
    print("Recognising topic for all pages...")
    start_time = time.time()
    length = 0
    for page_id in page_ids:
        if page_id == "TheSmartLocal":
            continue
        print(page_id)
        add_topic(page_id)
        length += shape
    end_time = time.time()
    elapsed_time = end_time - start_time
    ov_speed = length/elapsed_time
    log = "Finished recognising topics for all pages! Elapsed time: {}\n"\
        .format(elapsed_time)
    log += "Overall samples per second = " + str(ov_speed)
    print(log)
    du.write_text_to_txt(log, LOGGING_TOPIC_FILENAME)


if __name__ == "__main__":
    add_topic_to_all_pages()
