from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.neural_network import MLPClassifier 
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from server.core.data_preprocessing import extract_features, corpus
import pandas as pd
import numpy as np
import nltk
import time


def train(vocab_dict, train_url, classifier):
    global train_tf
    global train_label
    global clf
    global vocab
    global r
    vocab=vocab_dict

    df_train = pd.read_csv(train_url)
    train_post = df_train.loc[:, ["message+desc"]]
    train_post = list(train_post.values.flatten())
    train_label = df_train.loc[:, ["class_label"]]
    train_label = list(train_label.values.flatten())
    #train_tf = df_train.loc[:, vocab]
    train_tf = df_train.as_matrix(vocab)
    print(train_tf)
    r = 3*len(train_post)//5

    """
    vocab = food + events + nature + accommodation + attraction
    vocab = list(set(vocab))
    vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())

    train_count = vectorizer.fit_transform(train_post)
    bagOfWord = train_count.toarray()

    tf_transformer = TfidfTransformer(use_idf=False).fit(train_count)
    train_tf = tf_transformer.transform(train_count)


    n_features = len(bagOfWord[0])
    """

    if classifier == 1:
    	clf = MultinomialNB()
    elif classifier == 2:
    	clf = RandomForestClassifier(n_estimators = 110)
    elif classifier == 3:
    	clf = GaussianNB()
    elif classifier == 4:
    	clf = NearestCentroid()
    else:
    	clf = MLPClassifier()

    """TRAINING"""
    print(train_tf)
    print(train_tf[:r, :])
    clf.fit(train_tf[:r, :], train_label[:r])
    #rf = RandomForestClassifier(n_estimators = 110)
    #rf.fit(train_tf[:r, :], train_label[:r])


def validate():
    """VALIDATING"""

    result = clf.predict(train_tf[r:, :])
    #result = rf.predict(train_tf[r:, :])
    result = list(map(float, result))
    valRes = train_label[r:]
    valRes = list(map(float, valRes))

    """
    for i in range(len(result)):
    	print("class: " + str(valRes[i]) + " predicted: " + str(result[i]))
    """

    print("confusion_matrix")
    print(confusion_matrix(valRes, result))

    print("accuracy_score: " + str(accuracy_score(valRes, result)))

    target = ["Food", "Events", "Nature", "Accommodation", "Attraction", "Wrong"]
    print("classification_report")
    print(classification_report(valRes, result, target_names = target))
