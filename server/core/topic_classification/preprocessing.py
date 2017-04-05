from sklearn.model_selection import train_test_split
import pandas as pd
from server.utils import data_util

SEED = 42
RF_CLASSIFIER = "RF"
NB_CLASSIFIER = "NB"
NN_CLASSIFIER = "NN"

def get_all_data():
    """Compile all data, return X (raw features) and y (class label)"""
    print(data_util.get_labelled_csv_filepath("0"))
    # df0 = pd.read_csv("splitted_data_0.csv", usecols=[2, 11])
    # df1 = pd.read_csv("splitted_data_1.csv", usecols=[2, 11])
    # df2 = pd.read_csv("splitted_data_2.csv", usecols=[2, 11])
    # df3 = pd.read_csv("splitted_data_3.csv", usecols=[2, 11])
    # df4 = pd.read_csv("splitted_data_4.csv", usecols=[2, 11])
    # frames = [df1, df2, df3, df4]
    # pass


def split_train_test(X, y):
    """Split X and y into X_train, X_test, y_train, y_test"""
    return train_test_split(X, y, test_size=0.2, random_state=SEED)


def preprocess(X):
    """Accept X, preprocess X data return cleaned text"""
    pass


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
    get_all_data()