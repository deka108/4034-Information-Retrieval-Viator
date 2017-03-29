from server.core.data_preprocessing import preprocessing
from server.utils import data_util,text_util
import pandas as pd

def compute_words(file_name):
    df = data_util.get_csv_data(file_name)
    df["message_cleaned"] = df["message"].apply(
        lambda x: text_util.clean_text(x) if pd.notnull(x) else "")
    df["description_cleaned"] = df["description"].apply(
        lambda x: text_util.clean_text(x) if pd.notnull(x) else "")
    # print(df["message_cleaned"])
    message_word_count, message_unique_word_count = text_util.count_words(df["message_cleaned"])
    desc_word_count, desc_unique_word_count = text_util.count_words(df["description_cleaned"])
    total_word_count = message_word_count + desc_word_count
    total_unique_word_count = message_unique_word_count + desc_unique_word_count
    print("Total words: {}".format(total_word_count))
    print("Total unique words: {}".format(total_unique_word_count))

if __name__ == "__main__":
    compute_words(data_util.ALL_POSTS_COMMENTS_FILENAME)