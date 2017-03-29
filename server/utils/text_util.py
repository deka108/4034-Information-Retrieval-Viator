from datetime import datetime
from server.utils import data_util as du
from nltk.corpus import stopwords
import re

TEXT_COLUMNS = ["message", "description"]
stop_words = set(stopwords.words('english'))


def extract_date(time_info):
    data_obj = datetime.strptime(time_info, "%Y-%m-%dT%H:%M:%S%z")

    return data_obj.year, data_obj.strftime("%B"), data_obj.strftime("%A"), \
           (lambda x: (x % 6) == 0)(int(data_obj.strftime("%w")))


def clean_text(text):
    text = remove_http_symbols(text)
    text = text.lower()

    # removes extra space
    text = " ".join(word for word in text.split())

    return text


def remove_http_symbols(text):
    # remove hyperlink
    text = re.sub(r"https?[^\s]+", " ", text)
    text = re.sub(r"[^\s]+\.[^\s]+.[^\s]+", " ", text)

    # replace non alphabets
    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text


def count_words(df_text):
    results = set()
    word_count = df_text.str.split().apply(len).sum()
    df_text.str.split().apply(results.update)

    print("Total words: {}".format(word_count))
    print("Total unique words: {}".format(len(results)))


def get_text_data_by_page_id(page_id):
    data = du.get_csv_data_by_pageid(page_id)
    return get_text_data(data)


def get_text_data_all():
    data = du.get_all_posts_with_comments()
    return get_text_data(data)


def get_text_data(data):
    text_data = data[TEXT_COLUMNS]
    text_data = text_data.fillna("")
    text_data = text_data.apply(get_text, axis=1)
    return text_data


def preprocess_text(text):
    text = clean_text(text)
    return [word for word in text.split() if word not in stop_words]


def get_text(row):
    row['full_text'] = " ".join(row[col] for col in TEXT_COLUMNS)
    return row