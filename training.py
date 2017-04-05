from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.neural_network import MLPClassifier 
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score
from server.core.topic_classification import classification_preprocessing as cp
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

topic = {"vocab_food": "",
         "vocab_events": "",
         "vocab_nature": "",
         "vocab_acc": "",
         "vocab_attraction":""}

categories = ["food", "events", "nature", "accommodation", "attraction"]
df = pd.read_csv('./server/core/data_preprocessing/corpus_fromvocab.csv', names=categories).astype(str)

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

train_post, val_post, train_label, valRes = cp.run()
train_post = train_post.tolist()
train_label = train_label.tolist()
val_post = val_post.tolist()
valRes = valRes.tolist()

vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())

train_count = vectorizer.fit_transform(train_post)
val_count = vectorizer.fit_transform(val_post)
bagOfWord = train_count.toarray()

tf_transformer = TfidfTransformer(use_idf=False).fit(train_count)
train_tf = tf_transformer.transform(train_count)
val_transformer = TfidfTransformer(use_idf=False).fit(val_count)
val_tf = val_transformer.transform(val_count)

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

"""TESTING"""
test_df = pd.read_csv("./server/data/all_posts.csv", encoding='utf-8')

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

no = int(input("Enter page id: "))
if no==1:
	page_id = "TheSmartLocal"
elif no==2:
	page_id = "goturkeytourism"
elif no==3:
	page_id="incredibleindia"
elif no==4:
	page_id="indonesia.travel"
elif no==5:
	page_id="itsmorefuninthePhilippines"
elif no==6:
	page_id="koreatourism"
elif no==7:
	page_id = "malaysia.travel.sg"
elif no==8:
	page_id="visitchinanow"
elif no==9:
	page_id="visitjapaninternational"
else:
	page_id="wonderfulplacesindo"

test_data = test_df.loc[test_df["page_id"] == page_id]
test_data = test_data.loc[:, ["id", "page_id", "message", "description"]]
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

test_count = vectorizer.fit_transform(test_post)

test_transformer = TfidfTransformer(use_idf=False).fit(test_count)
test_tf = test_transformer.transform(test_count)

test_result = clf.predict(test_tf)

a = np.column_stack((test_post, test_result))

test_concat = np.concatenate((test_id, test_pg, a), axis=1)
predicted = pd.DataFrame(test_concat, columns = ["id", "page_id", "msg+dsc", "predicted_class"])

#test_data = test_data.join(class_lbl)
#test_data["predicted_class"]=pd.DataFrame(test_result[:], columns=["predicted_class"])

print(predicted["predicted_class"])
predicted.to_csv("predicted_class.csv", encoding='utf-8')