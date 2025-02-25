from server.core.data_preprocessing import preprocessing
from server.utils import data_util,text_util
import pandas as pd

def compute_words(file_name):
    # data_path = data_util.get_csv_filepath(file_name)
    df = data_util.get_csv_data_from_filename(file_name)
    df["message_cleaned"] = df["message"].apply(
        lambda x: text_util.clean_text(x) if pd.notnull(x) else "")
    df["description_cleaned"] = df["description"].apply(
        lambda x: text_util.clean_text(x) if pd.notnull(x) else "")
    # print(df["message_cleaned"])
    frames = [df["message_cleaned"],df["description_cleaned"]]
    combined = pd.concat(frames)
    total_word_count,total_unique_word_count = text_util.count_words(combined)
    print("Total words: {}".format(total_word_count))
    print("Total unique words: {}".format(total_unique_word_count))


def read_csv(file_name):
    df = data_util.get_csv_data_from_filename(file_name)
    print(type(df["message"][0]))

if __name__ == "__main__":
    compute_words(data_util.ALL_POSTS_FILENAME)
