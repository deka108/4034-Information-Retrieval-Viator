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


start_time = time.time()
class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]


nltk.data.path.append('D:/nltk_data/')

def create_vocab():
	topic = {"vocab_food": "",
         "vocab_events": "",
         "vocab_nature": "",
         "vocab_acc": "",
         "vocab_attraction":""}

	categories = ["food", "events", "nature", "accommodation", "attraction"]
	df = du.get_csv_data_from_filename("corpus_fromvocab")
	#df = pd.read_csv(corpus_file, names=categories).astype(str)

	food = df.food.tolist()
	food = list(filter(('nan').__ne__, food))

	events = df.events.tolist()
	events = list(filter(('nan').__ne__, events))

	nature = df.nature.tolist()
	nature = list(filter(('nan').__ne__, nature))

	accommodation = df.accommodation.tolist()
	accommodation = list(filter(('nan').__ne__, accommodation))

	attraction = df.attraction.tolist()
	attraction = list(filter(('nan').__ne__, attraction))

	vocab = food + events + nature + accommodation + attraction
	vocab = list(set(vocab))

	joblib.dump(vocab, 'vocab.pkl') 

def create_features():
	train_post, val_post, train_label, valRes = cp.run()
	train_post = train_post.tolist()
	train_label = train_label.tolist()
	val_post = val_post.tolist()
	valRes = valRes.tolist()

	vocab = joblib.load('vocab.pkl')
	vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())

	train_count = vectorizer.fit_transform(train_post)
	val_count = vectorizer.fit_transform(val_post)
	bagOfWord = train_count.toarray()

	tf_transformer = TfidfTransformer(use_idf=False).fit(train_count)
	train_tf = tf_transformer.transform(train_count)
	val_transformer = TfidfTransformer(use_idf=False).fit(val_count)
	val_tf = val_transformer.transform(val_count)

	return train_tf, val_tf, train_label, valRes

def create_model():

	train_tf, val_tf, train_label, valRes = create_features()
	
	clf = RandomForestClassifier(n_estimators = 110)
	clf.fit(train_tf[:, :], train_label[:])

	result = clf.predict(val_tf[:, :])
	result = list(map(float, result))
	valRes = list(map(float, valRes))

	print("confusion_matrix")
	print(confusion_matrix(valRes, result))

	print("accuracy_score: " + str(accuracy_score(valRes, result)))

	target = ["Food", "Events", "Nature", "Accommodation", "Attraction", "Wrong"]
	print("classification_report")
	print(classification_report(valRes, result, target_names = target))

	joblib.dump(clf, 'rf_tfidf.pkl')


def predict(page_id):
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

def run_once():
	create_vocab()
	create_model()

if __name__ == "__main__":
	#only need to run this once to generate pickle files
	#run_once()

	print("1. TheSmartLocal")
	print("2. goturkeytourism")
	print("3. incredibleindia")
	print("4. indonesia.travel")
	print("5. itsmorefuninthePhilippines")
	print("6. koreatourism")
	print("7. malaysia.travel.sg")
	print("8. visitchinanow")
	print("9. visitjapaninternational")
	print("10. wonderfulplacesindo")

	page_id = str(input("Enter page id: "))
	predict(page_id)
