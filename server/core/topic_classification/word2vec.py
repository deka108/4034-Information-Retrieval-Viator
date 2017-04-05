from sklearn.model_selection import train_test_split
import pandas as pd
from server.utils import data_util,text_util
from nltk.tokenize import sent_tokenize, word_tokenize
from server.core.topic_classification import classification_preprocessing

SEED = 42
RF_CLASSIFIER = "RF"
NB_CLASSIFIER = "NB"
NN_CLASSIFIER = "NN"

def preprocess(X):
    """Accept X, preprocess X data return cleaned text"""
    clean_sentence_list= []
    message_list = X.tolist()
    for message in message_list:
        sentence = sent_tokenize(message)
        clean_sentence = [text_util.clean_text(x) for x in sentence]
        # print(clean_sentence)
        clean_sentence_list += clean_sentence
    return clean_sentence_list

def generate_features(X):
    """Accept cleaned text, and generate features to be trained for the
    classifiers"""
    pass


def train_classifier(X, y, classifier_model):
    """Generate trained model from the features, save the model. Use either
    naive bayes, rf or neural network"""
    if classifier_model == RF_CLASSIFIER:
        pass
    elif classifier_model == NB_CLASSIFIER:
        pass
    elif classifier_model == NN_CLASSIFIER:
        pass

    pass


def predict_test(X_train, y_train, X_test, y_test):
    """Predict test labels, compute accuracy bla bla (see the assignment
    pdf)"""
    pass

if __name__ == "__main__":
    X_train, X_test, y_train, y_test = classification_preprocessing.run()
    print(X_train, X_test, y_train, y_test)