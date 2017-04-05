from sklearn.model_selection import train_test_split
import pandas as pd

from server.core.topic_classification.classifier import RFClassifier, \
    NBClassifier, NNClassifier
from server.utils import data_util,text_util
from nltk.tokenize import sent_tokenize, word_tokenize
from server.core.topic_classification import classification_preprocessing
from gensim.models import Word2Vec,word2vec
import logging

SEED = 42
RF_CLASSIFIER = "RF"
NB_CLASSIFIER = "NB"
NN_CLASSIFIER = "NN"
DOCUMENT_MAX_NUM_WORDS = 100
NUM_FEATURES = 300  # Word vector dimensionality


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


def generate_features(X):
    """Accept cleaned text, and generate features to be trained for the
    classifiers"""
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', \
                        level=logging.INFO)

    min_word_count = 40  # Minimum word count
    num_workers = 4  # Number of threads to run in parallel
    context = 10  # Context window size
    downsampling = 1e-3  # Downsample setting for frequent words

    print("Training model...")
    model = word2vec.Word2Vec(X, workers=num_workers, \
                              size=NUM_FEATURES, min_count=min_word_count, \
                              window=context, sample=downsampling)
    model.init_sims(replace=True)
    model_name = "word2vec_features"
    model.save(model_name)


def train_classifier(X_train, y_train, classifier_model):
    """Generate trained model from the features, save the model. Use either
    naive bayes, rf or neural network"""
    if classifier_model == RF_CLASSIFIER:
        classifier = RFClassifier()
    elif classifier_model == NB_CLASSIFIER:
        classifier = NBClassifier()
    elif classifier_model == NN_CLASSIFIER:
        classifier = NNClassifier()

    classifier.train_model(X_train, y_train)


def predict_test(X_train, y_train, X_test, y_test):
    """Predict test labels, compute accuracy bla bla (see the assignment
    pdf)"""
    pass

if __name__ == "__main__":
    X,y = classification_preprocessing.get_all_data()
    X_clean = preprocess(X)
    generate_features(X_clean)
    model = word2vec.load("word2vec_features")
