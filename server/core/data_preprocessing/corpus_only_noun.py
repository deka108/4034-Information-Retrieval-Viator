import nltk
import pandas as pd
import numpy as np
import csv 
from itertools import zip_longest
from nltk.corpus import wordnet as wn
from nltk import word_tokenize, pos_tag

nltk.data.path.append('D:/nltk_data/')

topic = {"vocab_food": "",
         "vocab_events": "",
         "vocab_nature": "",
         "vocab_acc": "",
         "vocab_attraction":""}

df = pd.read_csv("vocab.csv")
topic["vocab_food"] = df.as_matrix(["food"]).astype(str)
topic["vocab_events"] = df.as_matrix(["events"]).astype(str)
topic["vocab_nature"] = df.as_matrix(["nature"]).astype(str)
topic["vocab_acc"] = df.as_matrix(["accommodation"]).astype(str)
topic["vocab_attraction"] = df.as_matrix(["attraction"]).astype(str)

corpus_food = []
corpus_events = []
corpus_nature = []
corpus_acc = []
corpus_attraction = []

for cl in topic.keys() :
    temp = list()
    for word in topic[cl]:
        for syn in wn.synsets(word[0]):
            if word[0] != 'nan':
                for l in syn.lemmas():
                    temp.append(l.name())
                    if l.antonyms():
                        continue
            else:
                continue
    if cl=="vocab_food":
        corpus_food = list(temp)
    elif cl=="vocab_events":
        corpus_events = list(temp)
    elif cl=="vocab_nature":
        corpus_nature=list(temp)
    elif cl=="vocab_acc":
        corpus_acc = list(temp)
    else:
        corpus_attraction = list(temp)

print (len(corpus_food) + len(corpus_events) + len(corpus_nature) + len(corpus_acc) + len(corpus_attraction))

food = list(set(corpus_food))
events = list(set(corpus_events))
nature = list(set(corpus_nature))
acc = list(set(corpus_acc))
attraction = list(set(corpus_attraction))

print(len(food))

food_stc = " ".join(food)
events_stc = " ".join(events)
nature_stc = " ".join(nature)
acc_stc = " ".join(acc)
attraction_stc = " ".join(attraction)

"""
food_token = word_tokenize(food_stc)
events_token = word_tokenize(events_stc)
nature_token = word_tokenize(nature_stc)
acc_token = word_tokenize(acc_stc)
attraction_token = word_tokenize(attraction_stc)

food_tag = nltk.pos_tag(food_token)
events_tag = nltk.pos_tag(events_token)
nature_tag = nltk.pos_tag(nature_token)
acc_tag = nltk.pos_tag(acc_token)
attraction_tag = nltk.pos_tag(attraction_token)
"""

"""FOOD"""

food_N = [token for token, pos in pos_tag(word_tokenize(food_stc)) if pos.startswith('N') or pos == 'VB']

print(len(food_N))

for word in food:
    if word not in food_N:
        print(word)
"""

corpus = [food, events, nature, acc, attraction]
cols = ["food", "events", "nature", "accommodation", "attraction"]

with open("corpus.csv","w") as f:
    writer = csv.writer(f)
    writer.writerow(cols)
    for values in zip_longest(*corpus):
        writer.writerow(values)
"""