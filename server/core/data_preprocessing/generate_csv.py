import pandas as pd
import numpy as np
from server.utils import data_util
from server.core.data_preprocessing import topic_labeling

def generate_ordered_csv():
    data_path = data_util.get_csv_filepath(data_util.ALL_POSTS_COMMENTS_FILENAME)

    cols = ["id", "message", "description", "comments"]

    df = pd.read_csv(data_path, encoding="utf-8").astype(str)
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
    df_write.to_csv(data_util.get_csv_filepath(data_util.ORDERED_DATA_FILENAME),
                    encoding='utf-8', index_label="no")

    print("ordered_data.csv successfully generated")


def shuffle_data():
    csv_column = ['id', 'message+desc', 'comments']

    df = pd.read_csv(data_util.get_csv_filepath(data_util.ORDERED_DATA_FILENAME))
    matrix = df.as_matrix(csv_column)
    shuffled = df.sample(frac=1, random_state = 42)
    df2 = pd.DataFrame(shuffled, columns = csv_column)
    df2.to_csv(data_util.get_csv_filepath(data_util.SHUFFLED_DATA_FILENAME),
               encoding='utf-8', index_label="no")

    print("shuffled_data.csv successfully generated")


def split_csv():
    data_path = data_util.get_csv_filepath(data_util.TOPIC_LABELLED_FILENAME)

    csv_column = ['id', 'message+desc', "comments", "count_food", "count_events", "count_nature", 
            "count_accommodation", "count_attraction", "count_others", "class_label"]
    shuffled = pd.read_csv(data_path, encoding='utf-8').iloc[:, 1:].astype(str)
    data = np.array_split(shuffled, 5)
 
    for i in range(len(data)):
        df3 = pd.DataFrame(data[i], columns = csv_column)
        df3.to_csv(data_util.get_splitted_csv_filepath(i), encoding='utf-8',\
        index_label="no")

    print("csvs successfully splitted")


def generate_splitted_csv_for_labelling():
    generate_ordered_csv()
    shuffle_data()
    topic_labeling.label_data()
    split_csv()


if __name__ == "__main__":
    generate_ordered_csv()
    shuffle_data()
    topic_labeling.label_data()
    split_csv()
