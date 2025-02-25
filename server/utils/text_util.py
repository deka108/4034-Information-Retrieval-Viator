from datetime import datetime
from server.utils import data_util as du
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize, RegexpTokenizer
import re
import string


printable = set(string.printable)
stop_words = set(stopwords.words('english'))
stemmer = SnowballStemmer('english')
lemmatizer = WordNetLemmatizer()
regexp_tokenizer = RegexpTokenizer('[\'a-zA-Z]+')

TEXT_COLUMNS = ["message", "description"]
EXTRACTED_COLUMNS = TEXT_COLUMNS + ["id", "page_id"]


def get_text_data_by_page_id(page_id):
    data = du.get_csv_data_by_pageid(page_id)
    return get_text_data(data)


def get_text_data_all():
    data = du.get_all_posts()
    return get_text_data(data)


def get_text_data(data):
    text_data = data[EXTRACTED_COLUMNS]
    text_data = text_data.fillna("")
    text_data = text_data.apply(get_text, axis=1)
    return text_data


def get_text(row):
    row['full_text'] = " ".join(row[col] for col in TEXT_COLUMNS)
    row['full_text'] = remove_hyperlink(row['full_text'])
    row['full_text'] = "".join(filter(lambda x: x in printable,
                                      row['full_text']))
    return row


def preprocess_text(text, stem=False, lemmatize=False, rebuild_text=False):
    # Cleaning: remove hyperlinks and symbols
    text = clean_text(text)

    # Normalization: either lemmatize using wordnet lemmatizer or stemming
    # using snowballstemmer
    if lemmatize:
        return [lemmatizer.lemmatize(word) for word in text.split() if word
                not in stop_words]
    if stem:
        return [stemmer.stem(word) for word in text.split() if word not in
                    stop_words]

    # Removing stopwords
    tokens = [word for word in text.split() if word not in stop_words]

    if rebuild_text:
        return " ".join(tokens)

    return tokens


def clean_text(text):
    # Remove hyperlinks and symbols
    text = remove_http_symbols(text)

    # Case folding
    text = text.lower()

    # removes extra space
    text = " ".join(word for word in text.split())

    return text


def tokenize(text):
    words = []

    for sentence in sent_tokenize(text):
        tokens = [lemmatizer.lemmatize(t.lower())
                  for t in regexp_tokenizer.tokenize(sentence) if
                  t.lower() not in stop_words]
        words += tokens

    return words


def remove_http_symbols(text):
    # remove hyperlink
    text = remove_hyperlink(text)

    # replace non alphabets
    text = re.sub(r"[^a-zA-Z]", " ", text)
    return text


def remove_hyperlink(text):
    text = re.sub(r"https?[^\s]+", " ", text)
    text = re.sub(r"[^\s]+\.[^\s]+.[^\s]+", " ", text)
    return text


def count_words(df_text):
    results = set()
    word_count = df_text.str.split().apply(len).sum()
    df_text.str.split().apply(results.update)
    unique_word_count = len(results)
    return word_count, unique_word_count
    # print("Total words: {}".format(word_count))
    # print("Total unique words: {}".format(len(results)))


def extract_date(time_info):
    data_obj = datetime.strptime(time_info, "%Y-%m-%dT%H:%M:%S%z")

    return data_obj.year, data_obj.strftime("%B"), data_obj.strftime("%A"), \
           (lambda x: (x % 6) == 0)(int(data_obj.strftime("%w")))
