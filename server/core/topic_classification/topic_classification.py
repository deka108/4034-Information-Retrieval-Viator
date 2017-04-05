from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.neural_network import MLPClassifier 
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score
from sklearn.externals import joblib
from server.core.topic_classification import classification_preprocessing as cp
from server.utils import data_util as du
import pandas as pd
import numpy as np
import nltk
import time
import pickle

class LemmaTokenizer(object):
	def __init__(self):
	    self.wnl = WordNetLemmatizer()
	def __call__(self, doc):
	    return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

# nltk.data.path.append('D:/nltk_data/')

def add_topic(page_id):
	"""TESTING"""
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

	vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())
	test_count = vectorizer.fit_transform(test_post)

	test_transformer = TfidfTransformer(use_idf=False).fit(test_count)
	test_tf = test_transformer.transform(test_count)

	test_result = clf.predict(test_tf)

	test_result = list(map(float, test_result))
	test_result = list(map(int, test_result))

	id_result = np.column_stack((test_id, test_result))

	result_df = pd.DataFrame(id_result, columns=["id", "predicted_class"])

	predicted = test.merge(result_df, on="id")
	headers = ["predicted_class"]

	filename = page_id + "_facebook"
	du.write_df_to_existing_csv(predicted, headers, filename)
	print("predicted class saved to " + filename)
	#1. Food
	#2. Event
	#3. Nature
	#4. Accommodation
	#5. Attraction

def add_topic_to_all_pages():
    page_ids = du.get_page_ids()
    for page_id in page_ids:
    	add_topic(page_id)


if __name__ == "__main__":
    add_topic_to_all_pages()