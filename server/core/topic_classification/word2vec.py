from sklearn.model_selection import train_test_split
import pandas as pd

from server.core.topic_classification.classifier import RFClassifier, \
    NBClassifier, NNClassifier
from server.utils import data_util,text_util
from nltk.tokenize import sent_tokenize, word_tokenize
from server.core.topic_classification import classification_preprocessing
from gensim.models import Word2Vec,word2vec
import logging
import numpy as np

SEED = 42
RF_CLASSIFIER = "RF"
NB_CLASSIFIER = "NB"
NN_CLASSIFIER = "NN"
DOCUMENT_MAX_NUM_WORDS = 100
NUM_FEATURES = 300  # Word vector dimensionality


NUM_FEATURES = 300  # Word vector dimensionality
MIN_WORD_COUNT = 40  # Minimum word count
NUM_WORKERS = 4  # Number of threads to run in parallel
CONTEXT = 10  # Context window size
DOWNSAMPLING = 1e-3  # Downsample setting for frequent words

def get_all_data():
    """Compile all data, return X (raw features) and y (class label)"""
    # print(data_util.get_labelled_csv_filepath(0))
    df0 = pd.read_csv(data_util.get_labelled_csv_filepath(0), usecols=[2, 11])
    df1 = pd.read_csv(data_util.get_labelled_csv_filepath(1), usecols=[2, 11])
    df2 = pd.read_csv(data_util.get_labelled_csv_filepath(2), usecols=[2, 11])
    df3 = pd.read_csv(data_util.get_labelled_csv_filepath(3), usecols=[2, 11])
    df4 = pd.read_csv(data_util.get_labelled_csv_filepath(4), usecols=[2, 11])
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
    message_list = X.tolist()
    for message in message_list:
        sentence = sent_tokenize(message)
        clean_sentence = [text_util.preprocess_text(x,lemmatize=True) for x in sentence]
        # print(clean_sentence)
        clean_sentence_list += clean_sentence
    return clean_sentence_list

def create_model(sentences):
    """Accept cleaned text, and generate features to be trained for the
    classifiers"""
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                        level=logging.INFO)

    print("Training model...")
    model = word2vec.Word2Vec(sentences, workers=NUM_WORKERS, \
                              size=NUM_FEATURES, min_count=MIN_WORD_COUNT, \
                              window=CONTEXT, sample=DOWNSAMPLING)
    model.init_sims(replace=True)
    model_name = "word2vec_features"
    model.save(model_name)

def generate_features(X):
    clean_train_posts = []
    pass

def makeFeatureVec(words,model,num_features):
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0.
    index2word_set = set(model.index2word)
    for word in words:
        if word in index2word_set:
            nwords = nwords + 1.
            featureVec = np.add(featureVec, model[word])
    featureVec = np.divide(featureVec, nwords)
    return featureVec

def getAvgFeatureVecs(posts, model, num_features):
    counter = 0.
    reviewFeatureVecs = np.zeros((len(posts), num_features), dtype="float32")
    for review in posts:
       if counter%1000. == 0.:
           print ("Review %d of %d" % (counter, len(posts)))

       reviewFeatureVecs[counter] = makeFeatureVec(review, model, \
           num_features)
       counter = counter + 1.
    return reviewFeatureVecs

def train_classifier(X_train, y_train, X_test, y_test, classifier_model):
    """Generate trained model from the features, save the model. Use either
    naive bayes, rf or neural network"""
    if classifier_model == RF_CLASSIFIER:
        classifier = RFClassifier()
    elif classifier_model == NB_CLASSIFIER:
        classifier = NBClassifier()
    elif classifier_model == NN_CLASSIFIER:
        classifier = NNClassifier()

    classifier.train_model(X_train, y_train, X_test, y_test)


def predict_test(X_train, y_train, X_test, y_test):
    """Predict test labels, compute accuracy bla bla (see the assignment
    pdf)"""
    pass

def run():
    X,y = get_all_data()
    X_clean = preprocess(X)
    create_model(X_clean)
    model = word2vec.Word2Vec.load("word2vec_features")

if __name__ == "__main__":
    run()