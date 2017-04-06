from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.linear_model import LogisticRegression
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
	#train_post, val_post, train_label, valRes = cp.run()
	train, val = cp.get_all_data()
	#train_post = train_post.tolist()
	train_label = train_label.tolist()
	#val_post = val_post.tolist()
	valRes = valRes.tolist()

	vocab = joblib.load('vocab.pkl')
	print("length of vocab: " + str(len(vocab)))
	vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())

	train_count = vectorizer.fit_transform(train_post)
	val_count = vectorizer.fit_transform(val_post)


	tf_transformer = TfidfTransformer(use_idf=True).fit(train_count)
	train_tf = tf_transformer.transform(train_count)
	val_transformer = TfidfTransformer(use_idf=True).fit(val_count)
	val_tf = val_transformer.transform(val_count)


	return train_tf, val_tf, train_label, valRes

def create_model():

	train_tf, val_tf, train_label, valRes = create_features()

	clf1 = RandomForestClassifier(n_estimators = 110, random_state=1)
	clf2 = MultinomialNB()
	clf3 = LogisticRegression(random_state=1)
	
	clf = VotingClassifier(estimators=[('rf', clf1), ('mnb', clf2), ('lr', clf3)], voting='hard')
	train_label = list(map(float, train_label))
	train_label = list(map(int, train_label))
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


def run():
	create_vocab()
	create_model()

if __name__ == "__main__":
	run()