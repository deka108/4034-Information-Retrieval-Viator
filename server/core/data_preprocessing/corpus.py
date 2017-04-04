import nltk
import pandas as pd
import numpy as np
import csv 
from itertools import zip_longest
from nltk.corpus import wordnet as wn

nltk.data.path.append('D:/nltk_data/')

def extract_corpus(url):
    topic = {"vocab_food": "",
             "vocab_events": "",
             "vocab_nature": "",
             "vocab_acc": "",
             "vocab_attraction":""}


    df = pd.read_csv(url)

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
            if word[0] != 'nan':
                for syn in wn.synsets(word[0]):
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

    corpus = [food, events, nature, acc, attraction]
    for i in range(len(corpus)):
        for word in corpus[i]:
            if word=="nan":
                print("nan")
                
    cols = ["food", "events", "nature", "accommodation", "attraction"]

    filename = "./server/core/data_preprocessing/corpus_from" + url.replace("./server/core/data_preprocessing/", "")
    with open(filename,"w") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        for values in zip_longest(*corpus):
            writer.writerow(values)

    return filename

if __name__ == "__main__":
    url = "vocab.csv"
    corpus_file = extract_corpus(url)
    print(corpus_file)