import pandas as pd
import numpy as np
import os
from server.core.data_preprocessing import topic_labeling

def csv_to_csv():
    url = './server/data/all_posts_with_comments.csv'
    

    f = ['Tripviss_facebook.csv']

    cols = ["id", "message", "description", "comments"]

    df = pd.read_csv(url, encoding="utf-8").astype(str)
    postID = df.as_matrix([cols[0]])
    message = df.as_matrix([cols[1]])
    desc = df.as_matrix([cols[2]])
    post = list()
    for i in range(len(message)):
        post.append(message[i][0] + desc[i][0].replace("nan", " "))

    post = np.array_split(post, len(message))
    comments = df.as_matrix([cols[3]])
    #post = np.column_stack((message,desc))
    #print(post)
    comb = np.concatenate((postID, post, comments), axis=1)
    #print(comb)

    df_write = pd.DataFrame(comb, columns =["id", "message+desc", "comments"])
    df_write.to_csv("./server/core/data_preprocessing/ordered_data.csv", encoding='utf-8')

    print("ordered_data.csv successfully generated")


def shuffle_data():
    csv_column = ['id', 'message+desc', 'comments']

    df = pd.read_csv('./server/core/data_preprocessing/ordered_data.csv')
    matrix = df.as_matrix(csv_column)
    shuffled = df.sample(frac=1, random_state = 42)
    df2 = pd.DataFrame(shuffled, columns = csv_column)
    df2.to_csv('./server/core/data_preprocessing/shuffled_data.csv', encoding='utf-8')

    print("shuffled_data.csv successfully generated")

def split_csv():
    url = "./server/core/data_preprocessing/topic_labelled.csv"

    csv_column = ['id', 'message+desc', "comments", "count_food", "count_events", "count_nature", 
            "count_accommodation", "count_attraction", "count_others", "class_label"]
    shuffled = pd.read_csv(url, encoding='utf-8').iloc[:, 1:].astype(str)
    data = np.array_split(shuffled, 5)
 
    for i in range(len(data)):
        df3 = pd.DataFrame(data[i], columns = csv_column)
        df3.to_csv('./server/core/data_preprocessing/train_data' + str(i) + '.csv', encoding='utf-8')

    print("csvs successfully splitted")


if __name__ == "__main__":
    csv_to_csv()
    shuffled_data()
    label_data()
    split_csv()
