from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

from server.core.gensim_models.gensim_model import get_data
from server.utils import data_util, text_util
from nltk.tokenize import sent_tokenize
from collections import namedtuple

SEED = 42
RF_CLASSIFIER = "RF"
NB_CLASSIFIER = "NB"
NN_CLASSIFIER = "NN"
DOCUMENT_MAX_NUM_WORDS = 100
NUM_FEATURES = 300  # Word vector dimensionality
MIN_WORD_COUNT = 40  # Minimum word count
NUM_WORKERS = 4  # Number of threads to run in parallel
CONTEXT = 10  # Context window size
DOWNSAMPLING = 1e-3  # Downsample setting for frequent words


def get_all_data_with_name():
    """Compile all data, return X (raw features) and y (class label)"""
    df_all = get_compiled_data()

    X_post = df_all["message+desc"]
    X_post = list(X_post.values.flatten())
    X_name = df_all["name"]
    X_name = list(X_name.values.flatten())
    X = list()
    for i in range(len(X_post)):
        temp = str(X_post[i]) + " " + str(X_name[i])
        X.append(temp)

    y = df_all["class_label"]
    y = y.astype(int)
    return X, y


def get_all_data():
    """Compile all data, return X (raw features) and y (class label)"""
    df_all = get_compiled_data()

    X = df_all["message+desc"]
    y = df_all["class_label"]
    y = y.astype(int)
    return X, y


def get_compiled_data():
    df0 = pd.read_csv(data_util.get_labelled_csv_filepath(0))
    df1 = pd.read_csv(data_util.get_labelled_csv_filepath(1))
    df2 = pd.read_csv(data_util.get_labelled_csv_filepath(2))
    df3 = pd.read_csv(data_util.get_labelled_csv_filepath(3))
    df4 = pd.read_csv(data_util.get_labelled_csv_filepath(4))
    frames = [df0, df1, df2, df3, df4]
    df_all = pd.concat(frames)
    df_all = df_all[pd.notnull(df_all["class_label"])]
    df_all = df_all.loc[df_all["class_label"] != ' ']
    df_all.reset_index(drop=True, inplace=True)
    # print(df_all)
    data_util.write_df_to_csv(df_all, df_all.columns, "all_labelled_data")
    return df_all


def split_train_test(X, y, random=False):
    """Split X and y into X_train, X_test, y_train, y_test"""
    if random:
        return train_test_split(X, y, test_size=0.2)
    return train_test_split(X, y, test_size=0.2, random_state=SEED)


def run(with_name=True):
    if with_name:
        X, y = get_all_data_with_name()
    else:
        X, y = get_all_data()
    X_train, X_test, y_train, y_test = split_train_test(X[:, None], y)
    return X_train, X_test, y_train, y_test


def preprocess(X):
    """Accept X, preprocess X data return cleaned text in sentences"""
    clean_sentence_list= []
    message_list = X.tolist()
    for message in message_list:
        sentence = sent_tokenize(message)
        clean_sentence = [text_util.preprocess_text(token, lemmatize=True)
                          for token in sentence]
        # print(clean_sentence)
        clean_sentence_list += clean_sentence
    return clean_sentence_list


def preprocess_posts(X):
    """Accept X, preprocess X data return cleaned posts"""
    clean_posts_list = []
    message_list = X.tolist()
    for message in message_list:
        words = []
        for sentence in sent_tokenize(message):
            words += text_util.preprocess_text(sentence, lemmatize=True)
        # print(clean_sentence)
        clean_posts_list.append(words)
    return clean_posts_list


def preprocess_docs(X):
    """Accept X, preprocess X data return cleaned docs"""
    all_docs = []
    PostDocument = namedtuple("PostDocument", "words tags")
    message_list = X.tolist()
    for i, message in enumerate(message_list):
        words = text_util.preprocess_text(message, lemmatize=True)
        tags = [i]
        all_docs.append(PostDocument(words, tags))
    return all_docs


def get_cleaned_docs():
    X = get_data()
    return preprocess_docs(X)


def get_labels():
    return get_all_data()[1]


def get_posts():
    X = get_data()
    sentences = preprocess_posts(X)
    # for sentence in sentences:
    #     for token in sentence:
    #         if token in freq:
    #             freq[token] += 1
    #         else:
    #             freq[token] = 1
    # sentences = [[token for token in sentence if freq[token] > 1] for
    #              sentence in sentences]
    return sentences


if __name__ == "__main__":
    run()