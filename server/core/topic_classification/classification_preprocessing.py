from sklearn.model_selection import train_test_split
import pandas as pd
from server.utils import data_util,text_util
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.stem import WordNetLemmatizer

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

lemmatizer = WordNetLemmatizer()

def get_all_data_with_name():
    """Compile all data, return X (raw features) and y (class label)"""
    df0 = pd.read_csv(data_util.get_labelled_csv_filepath(0))
    df1 = pd.read_csv(data_util.get_labelled_csv_filepath(1))
    df2 = pd.read_csv(data_util.get_labelled_csv_filepath(2))
    df3 = pd.read_csv(data_util.get_labelled_csv_filepath(3))
    df4 = pd.read_csv(data_util.get_labelled_csv_filepath(4))

    frames = [df0,df1, df2, df3, df4]
    df_all = pd.concat(frames)
    df_all = df_all[pd.notnull(df_all["class_label"])]
    df_all = df_all.loc[df_all["class_label"] != ' ']
    df_all.reset_index(drop=True,inplace=True)
    # print(df_all)
    data_util.write_df_to_csv(df_all,df_all.columns,"all_labelled_data")

    X = df_all["message+desc"]
    X_post = df_all["message+desc"]
    X_post = list(X_post.values.flatten())
    X_name = df_all["name"]
    X_name = list(X_name.values.flatten())
    X = list()
    for i in range(len(X_post)):
        temp = str(X_post[i]) + str(X_name[i])
        X.append(temp)


    y = df_all["class_label"]
    return X,y

def get_all_data():
    """Compile all data, return X (raw features) and y (class label)"""
    df0 = pd.read_csv(data_util.get_labelled_csv_filepath(0))
    df1 = pd.read_csv(data_util.get_labelled_csv_filepath(1))
    df2 = pd.read_csv(data_util.get_labelled_csv_filepath(2))
    df3 = pd.read_csv(data_util.get_labelled_csv_filepath(3))
    df4 = pd.read_csv(data_util.get_labelled_csv_filepath(4))

    frames = [df0,df1, df2, df3, df4]
    df_all = pd.concat(frames)
    df_all = df_all[pd.notnull(df_all["class_label"])]
    df_all = df_all.loc[df_all["class_label"] != ' ']
    df_all.reset_index(drop=True,inplace=True)
    # print(df_all)
    data_util.write_df_to_csv(df_all,df_all.columns,"all_labelled_data")

    X = df_all["message+desc"]
    y = df_all["class_label"]
    return X,y

def split_train_test(X, y):
    """Split X and y into X_train, X_test, y_train, y_test"""
    return train_test_split(X, y, test_size=0.2, random_state=SEED)


def run():
    X,y = get_all_data_with_name()
    X_train, X_test, y_train, y_test = split_train_test(X[:, None],y)
    return X_train,X_test,y_train,y_test

if __name__ == "__main__":
    run()

