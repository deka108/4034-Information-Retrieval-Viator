from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer, PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import NearestCentroid
from sklearn.neural_network import MLPClassifier 
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, precision_score
import pandas as pd
import numpy as np
import nltk
import time


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
df = pd.read_csv('corpus_fromvocab.csv', names=categories).astype(str)

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


df0 = pd.read_csv("splitted_data_0.csv").loc[:, ["id", "message+desc", "class_label"]]
df1 = pd.read_csv("splitted_data_1.csv").loc[:, ["id", "message+desc", "class_label"]]
df2 = pd.read_csv("splitted_data_2.csv").loc[:, ["id", "message+desc", "class_label"]]
df3 = pd.read_csv("splitted_data_3.csv").loc[:, ["id", "message+desc", "class_label"]]
df4 = pd.read_csv("splitted_data_4.csv").loc[:, ["id", "message+desc", "class_label"]]

frames = [df0, df1, df2, df3, df4]
df_all = pd.concat(frames)
df_train = df_all.loc[pd.notnull(df_all["class_label"])]
df_train = df_train.loc[df_train["class_label"] != ' ']
print(len(df_train))


#train_post = df_train.as_matrix(["message+desc"])
train_post = df_train.loc[:, ["message+desc"]]
train_post = list(train_post.values.flatten())
train_label = df_train.loc[:, ["class_label"]]
train_label = list(train_label.values.flatten())



r = 3*len(train_post)//5


vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())

train_count = vectorizer.fit_transform(train_post)
bagOfWord = train_count.toarray()

tf_transformer = TfidfTransformer(use_idf=False).fit(train_count)
train_tf = tf_transformer.transform(train_count)

n_features = len(bagOfWord[0])

r = 3*len(train_post)//5

clf = RandomForestClassifier(n_estimators = 110)
clf.fit(train_tf[:r, :], train_label[:r])

result = clf.predict(train_tf[r:, :])
#result = rf.predict(train_tf[r:, :])
result = list(map(float, result))
valRes = train_label[r:]
valRes = list(map(float, valRes))

print("confusion_matrix")
print(confusion_matrix(valRes, result))

print("accuracy_score: " + str(accuracy_score(valRes, result)))

target = ["Food", "Events", "Nature", "Accommodation", "Attraction", "Wrong"]
print("classification_report")
print(classification_report(valRes, result, target_names = target))

"""TESTING"""
test_df = pd.read_csv("../../data/all_posts_with_comments.csv", encoding='utf-8')

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
test_message = test_data.loc[:, ["id", "message", "description"]]
test_post = pd.column_stack((test_message[:,1], test_message[:,2]))


train_count = vectorizer.fit_transform(train_post)
test_count = vectorizer.fit_transform(test_post)

test_transformer = TfidfTransformer(use_idf=False).fit(test_count)
test_tf = test_transformer.transform(test_count)

test_result = clf.predict(test_tf)

test_data["predicted_class"]=pd.DataFrame(test_result, columns=["predicted_class"])