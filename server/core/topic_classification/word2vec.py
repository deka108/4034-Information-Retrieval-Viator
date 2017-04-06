from sklearn.model_selection import train_test_split
import pandas as pd

from server.core.topic_classification.classifier import RFClassifier,NBClassifier,NNClassifier
from server.utils import data_util,text_util
from nltk.tokenize import sent_tokenize, word_tokenize
from server.core.topic_classification import classification_preprocessing as cf
from gensim.models import Word2Vec,word2vec
import logging
import numpy as np
from sklearn.ensemble import RandomForestClassifier

from bs4 import BeautifulSoup
import re
from nltk.corpus import stopwords
from sklearn import metrics
import nltk.data
from nltk.stem import WordNetLemmatizer
from sklearn.metrics import accuracy_score

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
lemmatizer = WordNetLemmatizer()
# Define a function to split a review into parsed sentences
def review_to_sentences( review, tokenizer, remove_stopwords=False ):
    # Function to split a review into parsed sentences. Returns a
    # list of sentences, where each sentence is a list of words
    #
    # 1. Use the NLTK tokenizer to split the paragraph into sentences
    raw_sentences = tokenizer.tokenize(review.strip())
    #
    # 2. Loop over each sentence
    sentences = []
    for raw_sentence in raw_sentences:
        # If a sentence is empty, skip it
        if len(raw_sentence) > 0:
            # Otherwise, call review_to_wordlist to get a list of words
            sentences.append( review_to_wordlist( raw_sentence, \
              remove_stopwords ))
    #
    # Return the list of sentences (each sentence is a list of words,
    # so this returns a list of lists
    return sentences

def review_to_wordlist( review, remove_stopwords=False ):
    # Function to convert a document to a sequence of words,
    # optionally removing stop words.  Returns a list of words.
    #
    # 1. Remove HTML
    review_text = BeautifulSoup(review).get_text()
    #
    # 2. Remove non-letters
    review_text = re.sub("[^a-zA-Z]"," ", review_text)

    #
    # 3. Convert words to lower case and split them
    words = review_text.lower().split()
    #
    # 4. Optionally remove stop words (false by default)
    if remove_stopwords:
        stops = set(stopwords.words("english"))
        words = [w for w in words if not w in stops]
        words = [lemmatizer.lemmatize(w) for w in words ]

    #
    # 5. Return a list of words
    return words


def get_all_data():
    """Compile all data, return X (raw features) and y (class label)"""
    # print(data_util.get_labelled_csv_filepath(0))
    df0 = pd.read_csv(data_util.get_labelled_csv_word2vec_filepath(0), usecols=[2, 11])
    df1 = pd.read_csv(data_util.get_labelled_csv_word2vec_filepath(1), usecols=[2, 11])
    df2 = pd.read_csv(data_util.get_labelled_csv_word2vec_filepath(2), usecols=[2, 11])
    df3 = pd.read_csv(data_util.get_labelled_csv_word2vec_filepath(3), usecols=[2, 11])
    df4 = pd.read_csv(data_util.get_labelled_csv_word2vec_filepath(4), usecols=[2, 11])
    frames = [df0,df1, df2, df3, df4]
    df_all = pd.concat(frames)
    df_all.reset_index(drop=True,inplace=True)
    # print(df_all)
    X = df_all["message+desc"]
    y = df_all["class_label"]
    return X,y


def preprocess(X):
    """Accept X, preprocess X data return cleaned text"""
    clean_sentence_list= []
    # message_list = X.tolist()
    for message in X:
        sentence = sent_tokenize(message)
        clean_sentence = [text_util.preprocess_text(x,lemmatize=True) for x in sentence]
        # print(clean_sentence)
        clean_sentence_list += clean_sentence
    return clean_sentence_list

def create_model(X_clean,y):
    """Accept cleaned text, and generate features to be trained for the
    classifiers"""
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                        level=logging.INFO)

    print("Training model...")
    model = word2vec.Word2Vec(X_clean, workers=cf.NUM_WORKERS, \
                              size=cf.NUM_FEATURES, min_count=cf.MIN_WORD_COUNT, \
                              window=cf.CONTEXT, sample=cf.DOWNSAMPLING)
    model.init_sims(replace=True)
    model_name = "word2vec_features"
    model.save(model_name)


def makeFeatureVec(words, model, num_features):
    featureVec = np.zeros((num_features,),dtype="float32")
    nwords = 0.
    index2word_set = set(model.wv.index2word)
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec,model[word])
    featureVec = np.divide(featureVec,nwords)
    return featureVec

def getAvgFeatureVecs(reviews, model, num_features):
    counter = 0.
    reviewFeatureVecs = np.zeros((len(reviews),num_features),dtype="float32")
    for review in reviews:
       if counter%1000. == 0.:
           print ("Review %d of %d" % (counter, len(reviews)))
       reviewFeatureVecs[int(counter)] = makeFeatureVec(review, model, \
           num_features)
       counter = counter + 1.
    return reviewFeatureVecs


def generate_features(model,X_train,X_test):
    clean_train_posts = []
    for sentence in X_train:
        print(sentence)
        clean_train_posts.append(review_to_wordlist(sentence))
    print("TEST")
    print(len(X_train))
    print(len(clean_train_posts))
    trainDataVecs = getAvgFeatureVecs(clean_train_posts,model,cf.NUM_FEATURES)
    print ("Creating average feature vecs for test")
    clean_test_posts = []
    for sentence in X_test:
        clean_test_posts.append(review_to_wordlist(sentence))
    testDataVecs = getAvgFeatureVecs(clean_test_posts,model,cf.NUM_FEATURES)
    return trainDataVecs, testDataVecs

# def train_classifier(X_train, y_train, X_test, y_test, classifier_model):
#     """Generate trained model from the features, save the model. Use either
#     naive bayes, rf or neural network"""
#     if classifier_model == cf.RF_CLASSIFIER:
#         classifier = RFClassifier()
#     elif classifier_model == cf.NB_CLASSIFIER:
#         classifier = NBClassifier()
#     elif classifier_model == cf.NN_CLASSIFIER:
#         classifier = NNClassifier()
#
#     classifier.train_model(X_train, y_train, X_test, y_test)


def predict_test(X_train, y_train, X_test, y_test):
    """Predict test labels, compute accuracy bla bla (see the assignment
    pdf)"""
    pass

def run_2():
    # TODAYYYY
    X_model,Y_model = get_all_data()
    X_clean = preprocess(X_model)
    create_model(X_clean, Y_model)
    model = Word2Vec.load("word2vec_features")
    X, y = cf.get_all_data_with_name()
    X_train, X_test, y_train, y_test = cf.split_train_test(X, y)
    clean_train_reviews = []
    clean_test_reviews = []
    for train_message in X_train:
        clean_train_reviews.append(review_to_wordlist(train_message, remove_stopwords=True))
    clean_train_reviews.pop(324)
    clean_train_reviews.pop(895)
    clean_train_reviews.pop(896)
    trainDataVecs = getAvgFeatureVecs(clean_train_reviews, model, cf.NUM_FEATURES)

    # trainDataVecs = np.delete(trainDataVecs,inds)

    print('STATISTICS')
    print(len(clean_train_reviews))
    print(len(clean_test_reviews))
    print(len(y_train))
    print(len(y_test))
    print(len(trainDataVecs))

    print(len(trainDataVecs))
    print("=========")
    for message in X_test:
        clean_test_reviews.append(review_to_wordlist(message, remove_stopwords=True))
        # clean_test_reviews.append(review_to_wordlist(message, remove_stopwords=True))
    print("TEST VALUE: ")
    print(len(clean_test_reviews))
    clean_test_reviews.pop(310)

    testDataVecs = getAvgFeatureVecs(clean_test_reviews, model, cf.NUM_FEATURES)
    inds = np.where(np.isnan(testDataVecs))
    print(inds)
    print(len(testDataVecs))
    y_train = y_train.drop(y_train.index[[324,895,896]])
    y_test = y_test.drop(y_test.index[310])
    y_train = y_train.apply(pd.to_numeric)
    y_test = y_test.apply(pd.to_numeric)

    forest = RFClassifier()
    forest.train_model(trainDataVecs,y_train,testDataVecs,y_test)
    result = forest.predict(testDataVecs,y_test)
    score = accuracy_score(y_test,result)
    print(score)



    # forest = RandomForestClassifier(n_estimators=100)
    # forest = forest.fit(trainDataVecs, y_train)
    # result = forest.predict(testDataVecs)
    # print(result)
    # score = accuracy_score(y_test, result)
    # print(score)


def run():
    #TODAYYYY
    X,y = cf.get_all_data_with_name()
    X_clean = preprocess(X)
    # print(X_clean)
    create_model(X_clean,y)
    model = Word2Vec.load("word2vec_features")
    X_train, X_test, y_train, y_test = cf.split_train_test(X,y)
    clean_train_reviews = []
    clean_test_reviews = []
    # X_train = preprocess(X_train)
    for train_message in X_train:
        clean_train_reviews.append(review_to_wordlist(train_message, remove_stopwords=True))
    # clean_train_reviews.pop(324)
    # clean_train_reviews.pop(895)
    # clean_train_reviews.pop(896)
    # print("TRAIN VALUE: ")
    # print((clean_train_reviews))
    # print()
    # print((clean_train_reviews[324]))
    # print((clean_train_reviews[1263]))
    trainDataVecs = getAvgFeatureVecs(clean_train_reviews,model,cf.NUM_FEATURES)
    # inds = np.where(np.isnan(trainDataVecs))
    # print(inds)
    # trainDataVecs = np.delete(trainDataVecs,inds)

    print(y_train)
    # y_train = y_train.drop(y_train.index[[324,895,896]])
    print('YTRAIN')
    print(len(clean_train_reviews))
    print(len(y_train))
    print(len(trainDataVecs))
    # print(y_train[324])
    # print(y_train[896])

    print(len(trainDataVecs))
    print("=========")
    for message in X_test:
        clean_test_reviews.append(review_to_wordlist(message,remove_stopwords=True))
    print("TEST VALUE: ")
    print(len(clean_test_reviews))
    testDataVecs = getAvgFeatureVecs(clean_test_reviews,model,cf.NUM_FEATURES)
    # testDataVecs = np.delete(testDataVecs, inds)
    trainDataVecs[np.isnan(trainDataVecs)] = 0
    testDataVecs[np.isnan(testDataVecs)] = 0
    print(len(testDataVecs))
    y_train = y_train.apply(pd.to_numeric)
    y_test = y_test.apply(pd.to_numeric)

    print("SHAPE:")
    print(trainDataVecs.shape)
    print(testDataVecs.shape)
    print(X_test.shape)
    print(X_train.shape)
    print(y_train.shape)
    print(y_test.shape)

    forest = RandomForestClassifier(n_estimators=100)
    forest = forest.fit(trainDataVecs,y_train)
    result = forest.predict(testDataVecs)
    print(result)
    score = accuracy_score(result,result)
    print(score)







    # #YESTERDAY
    # X_train, X_test, y_train, y_test = cf.run()
    # model = Word2Vec.load("word2vec_features")
    # trainDataVecs, testDataVecs= generate_features(model,X_train,X_test)
    # trainDataVecs[np.isnan(trainDataVecs)] = 0
    # testDataVecs[np.isnan(testDataVecs)] = 0
    #
    #
    # print(type(trainDataVecs))
    # print(type(testDataVecs))
    # print(trainDataVecs.shape)
    # print(testDataVecs.shape)
    # # train_inds = np.where(np.isnan(trainDataVecs))
    # # trainDataVecs[train_inds] = np.take(" ", train_inds[0])
    # # test_inds = np.where(np.isnan(testDataVecs))
    # # testDataVecs[test_inds] = np.take(" ",test_inds[0])
    # # # trainDataVecs = trainDataVecs[~np.isnan(trainDataVecs)]
    # # testDataVecs = testDataVecs[~np.isnan(testDataVecs)]
    #
    # print(trainDataVecs,testDataVecs)
    # # y_train = list(map(float, y_train))
    # # y_test = list(map(float, y_test))
    #
    # y_train = y_train.apply(pd.to_numeric)
    # y_test = y_test.apply(pd.to_numeric)
    #
    #
    # print("WHERE'S THE ERROR")
    # # print(X_test.shape)
    # # print(X_train.shape)
    # # print(y_train.shape)
    # # print(y_test.shape)
    #
    #
    # print(type(trainDataVecs))
    # forest = RandomForestClassifier(n_estimators=100)
    # forest = forest.fit(trainDataVecs, y_train)
    # result = forest.predict(testDataVecs)
    # # print(y_test.values)
    # print(result)
    # score = accuracy_score(y_test,result)
    # print(score)
    # # print(type(y_test))
    # # print(type(result))
    # # print(X_test)
    # # output = pd.DataFrame(data={"test_message": X_test, "label": result})
    # # output.to_csv("Word2Vec.csv", index=False, quoting=3)
if __name__ == "__main__":
    # run()
    run_2()

