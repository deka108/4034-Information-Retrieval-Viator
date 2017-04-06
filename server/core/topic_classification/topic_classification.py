from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
<<<<<<< HEAD
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score
from sklearn.externals import joblib
from server.core.topic_classification import classification_preprocessing as cp
from server.utils import data_util as du
from server import config
=======
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, \
    classification_report, precision_score
from sklearn.externals import joblib
from server.core.topic_classification import classification_preprocessing as cp
from server.utils import data_util as du, data_util
>>>>>>> 752c87e0ac945f2a9b827b3979cd2f8976a0d913
import pandas as pd
import numpy as np
import nltk
import time
import pickle

from server.utils.data_util import LOGGING_TOPIC_FILENAME


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()

    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


# nltk.data.path.append('D:/nltk_data/')

def add_topic(page_id):
    """TESTING"""
    print("Recognising topics for page:{}...".format(page_id))
    start_time = time.time()
    vocab = joblib.load('vocab.pkl')
    clf = joblib.load('rf_tfidf.pkl')

    test_df = du.get_csv_data_by_pageid(page_id)

    test = test_df.loc[test_df["page_id"] == page_id]
    test_data = test.loc[:, ["id", "page_id", "message", "description"]]
    test_id = test_data.loc[:, ["id"]]
    test_msg = test_data.loc[:, ["message"]]
    test_msg = test_msg.replace(np.nan, '', regex=True)
    test_msg = list(test_msg.values.flatten())
    test_desc = test_data.loc[:, ["description"]]
    test_desc = test_desc.replace(np.nan, '', regex=True)
    test_desc = list(test_desc.values.flatten())
    test_pg = test_data.loc[:, ["page_id"]]

    test_post = list()

    for i in range(len(test_msg)):
        temp = test_msg[i] + test_desc[i]
        test_post.append(temp)

    vectorizer = CountVectorizer(min_df=1, vocabulary=vocab,
                                 tokenizer=LemmaTokenizer())
    test_count = vectorizer.fit_transform(test_post)

    test_transformer = TfidfTransformer(use_idf=False).fit(test_count)
    test_tf = test_transformer.transform(test_count)

    test_result = clf.predict(test_tf)

    test_result = list(map(float, test_result))
    test_result = list(map(int, test_result))

    id_result = np.column_stack((test_id, test_result))
    end_time = time.time()
    elapsed_time = end_time - start_time
    log = "Finish recognising locations for page:{}! Elapsed Time: {}".format(
        page_id, elapsed_time)
    print(log)

<<<<<<< HEAD
	test_transformer = TfidfTransformer(use_idf=True).fit(test_count)
	test_tf = test_transformer.transform(test_count)


	test_result = clf.predict(test_tf)
=======
    result_df = pd.DataFrame(id_result, columns=["id", "predicted_class"])

    if "predicted_class" in test.columns:
        test.drop("predicted_class", axis=1, inplace=True)
>>>>>>> 752c87e0ac945f2a9b827b3979cd2f8976a0d913

    predicted = test.merge(result_df, on=["id"])

<<<<<<< HEAD
	print(test_post[0])
	print(test_result[0])

	id_result = np.column_stack((test_id, test_result))
=======
    filename = page_id + "_facebook"
    du.write_df_to_csv(predicted, predicted.columns, filename)
>>>>>>> 752c87e0ac945f2a9b827b3979cd2f8976a0d913

    print("Predicted class saved to " + filename)
    data_util.write_text_to_txt(log, LOGGING_TOPIC_FILENAME)

<<<<<<< HEAD
	"""
	if "predicted_class" in test.columns:
		test.drop("predicted_class", axis=1, inplace=True)
	"""
	predicted = test.merge(result_df, on=["id"])
	#print(predicted)

	filename = page_id + "_facebook"
	filepath = config.get_data_path(filename)
	predicted.to_csv(filepath, encoding='utf-8')
	#du.write_df_to_csv(predicted, predicted.columns, filename)
	print("predicted class saved to " + filename)
	#1. Food
	#2. Event
	#3. Nature
	#4. Accommodation
	#5. Attraction
=======

# 1. Food
# 2. Event
# 3. Nature
# 4. Accommodation
# 5. Attraction

>>>>>>> 752c87e0ac945f2a9b827b3979cd2f8976a0d913

	#TODO: classification time, samples per second

def add_topic_to_all_pages():
    page_ids = du.get_page_ids()
    print("Recognising topic for all pages...")
    start_time = time.time()
    for page_id in page_ids:
        add_topic(page_id)
    end_time = time.time()
    elapsed_time = end_time - start_time
    log = "Finished recognising topics for all pages! Elapsed time: {}"\
        .format(elapsed_time)
    print(log)
    data_util.write_text_to_txt(log, LOGGING_TOPIC_FILENAME)


if __name__ == "__main__":
    add_topic_to_all_pages()
