import pandas as pd
import csv
import datetime

from server.utils import text_util
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from server.utils import data_util

headers = ["message_desc","class_label",]
def preprocess_data():
    df0 = pd.read_csv("splitted_data_0.csv",usecols=[2,11])
    df1 = pd.read_csv("splitted_data_1.csv",usecols=[2,11])
    df2 = pd.read_csv("splitted_data_2.csv",usecols=[2,11])
    df3 = pd.read_csv("splitted_data_3.csv", usecols=[2, 11])
    df4 = pd.read_csv("splitted_data_4.csv", usecols=[2, 11])
    frames = [df0,df1,df2,df3,df4]
    df_all = pd.concat(frames)
    df_all = df_all[pd.notnull(df_all["class_label"])]
    df_all.to_csv("train.csv", index = False, header= False)
    df0.to_csv("test.csv",index=False,header=False)
    print("preprocess done")


def classify_data():
    list=[]
    with open("train.csv") as fp:
        for line in csv.reader(fp):
            # print(line)
            # re.sub(r'([^,0-9])\n', r'\1', string)
            # line.strip("\n")
            # list.append(tuple(line))
            # # re.sub()
            train = [(tuple(line)) for line in csv.reader(fp)]

    with open("test.csv") as f:
        for line in csv.reader(f):
            test = [(tuple(line)) for line in csv.reader(f)]
    print(list)
    print("start training")
    print(datetime.datetime.now())
    cl = NaiveBayesClassifier(train)
    print(datetime.datetime.now())
    accuracy = cl.accuracy(test)
    print(accuracy)

def classify():
    df = data_util.get_csv_data_from_filename(data_util.ALL_POSTS_FILENAME)
    blob = TextBlob(df["message "])
if __name__ == "__main__":
    preprocess_data()
    classify_data()