from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import json

class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

vocab_food = ["food", "restaurants", "meal", "delicious", "breakfast", "lunch",
              "dinner", "taste", "gastronomy", "dessert"]
vocab_events = ["event","festival", "concert", "carnaval", "fireworks", "new year",
                "christmas", "easter", "market", "celebrate", "show"]
vocab_nature = ["mountain", "hiking", "lake", "beach", "forest", "flower", "hill",
                "nature", "sea", "waterfall", "canyon", "cave", "river", "landscape"]
vocab_acc = ["hotel", "hostel", "motel", "inn", "stay", "night", "backpacker"]
vocab_attraction = ["museum", "park", "amusement park", "temple", "church", "bridge",
                    "mosque", "cruise", "pagoda", "shrine", "wall", "zoo", "aquarium",
                    "palace", "architecture"]

vocab = list()
vocab = vocab_food + vocab_events + vocab_nature + vocab_acc + vocab_attraction

vectorizer = CountVectorizer(min_df=1, vocabulary=vocab, tokenizer=LemmaTokenizer())

cl = {1:"Food", 2:"Events", 3:"Nature", 4:"Accomodation", 5:"Attraction", 6:"Other"}


#read from json
url = "./visitchinanow_facebook.json"

with open(url) as json_data:
    data = json.load(json_data)

message = list()
message_id = list()
for i in range(len(data)):
    temp = ""
    message_id.append(data[i]['id'])
    if 'message' in data[i]:
        temp += data[i]['message']
    if 'description' in data[i]:
        temp += data[i]['description']
    message.append(temp)

corpus = list(message)

csv_column = ['id', 'message+description']

comb = np.column_stack((message_id, message))

df = pd.DataFrame(comb, columns = csv_column)
df.to_csv('description_message.csv', index = False, encoding='utf-8')


#read csv files
#use panda to get the second column as a list
url_csv = "description_message.csv"

corpus_df = pd.read_csv(url_csv).astype(str)

corpus = corpus_df.iloc[:,1]

print (corpus)

bagOfWords = vectorizer.fit_transform(corpus)
bow_array = bagOfWords.toarray()

print(bow_array)

train_col = ['id'] + vocab

train_comb = np.column_stack((message_id, bow_array))

train_csv = pd.DataFrame(train_comb, columns = train_col)
train_csv.to_csv('train.csv', index = False)


#write to another csv file as a training data
#id    | features | class

#create another csv file for testing data

#training_data = array of features
#training_data_res = the class of each row

#clf = MultinomialNB().fit(training_data, training_data_res)

#predicted = clf.predict(val_data)

#print predicted







