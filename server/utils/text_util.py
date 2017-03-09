from datetime import datetime
import re


def extract_date(time_info):
    data_obj = datetime.strptime(time_info, "%Y-%m-%dT%H:%M:%S%z")

    return data_obj.year, data_obj.strftime("%M"), data_obj.strftime("%A"), \
           int(data_obj.strftime("%w"))


def clean_text(text):
    # remove hyperlink
    text = re.sub(r"https?://[^\s]+", " ", text)

    # replace non alphabets
    text = re.sub(r"[^a-zA-Z]", " ", text)
    text = text.lower()

    # removes extra space
    text = " ".join(word for word in text.split())
    return text


def count_words(df_text):
    results = set()
    word_count = df_text.str.split().apply(len).sum()
    df_text.str.split().apply(results.update)

    print("Total words: {}".format(word_count))
    print("Total unique words: {}".format(len(results)))