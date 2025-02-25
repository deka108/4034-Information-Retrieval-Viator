import time
from textblob import TextBlob
from server.utils import data_util
import pandas as pd
from guess_language import guess_language
from server import config
from server.utils.data_util import LOGGING_SENTIMENT_FILENAME

csv_headers = ["comments_sentiment","comments_subjectivity",]


def get_sentiment(page_id):
    print("Recognising sentiments for page:{}...".format(page_id))
    start_time = time.time()

    data= []
    counter = 0
    df = data_util.get_csv_data_by_pageid(page_id)

    comments = df["comments"]
    for comment in comments:
        # print(comment)
        entry = {}
        sentiment = []
        subjectivity_list = []
        if type(comment) is not float:
            if(guess_language(comment) == 'en'):
                if (isinstance(comment, str)):
                    comment = comment.split("$$")
                else:
                    comment = " "
                for sentence in comment:
                    comment_data = TextBlob(sentence)
                    polarity = comment_data.sentiment.polarity
                    subjectivity = comment_data.subjectivity
                    # print(subjectivity)
                    sentiment.append(polarity)
                    subjectivity_list.append(subjectivity)
                ave_sentiment = sum(sentiment)/(len(sentiment))
                ave_subjectivity = sum(subjectivity_list)/(len(subjectivity_list))
                counter += 1
                entry["comments_sentiment"] = ave_sentiment
                entry["comments_subjectivity"] = ave_subjectivity
            else:
                entry["comments_sentiment"] = 0
                entry["comments_subjectivity"] = 0
            data.append(entry)
    print(counter)
    # print(data)
    #return data
    end_time = time.time()
    elapsed_time = end_time - start_time
    log = "Finish recognising sentiments for page:{}! Elapsed Time: {}".format(
        page_id, elapsed_time)
    print(log)
    df_new = pd.DataFrame(data)
    # file_name = data_util.ALL_POSTS_COMMENTS_FILENAME
    dest_file_name = data_util.get_page_csv_filename(page_id)
    data_util.write_df_to_existing_csv(df_new, csv_headers, dest_file_name)
    data_util.write_text_to_txt(log, LOGGING_SENTIMENT_FILENAME)


def get_sentiment_all_pages():
    print("Recognising sentiment for all pages...")
    start_time = time.time()
    all_pageids = data_util.get_page_ids()
    for page_id in all_pageids:
        get_sentiment(page_id)
    end_time = time.time()
    elapsed_time = end_time - start_time
    log = "Finished recognising sentiment for all pages! Elapsed time: {}" \
        .format(elapsed_time)
    print(log)
    data_util.write_text_to_txt(log, LOGGING_SENTIMENT_FILENAME)


def run():
    get_sentiment_all_pages()

if __name__ == "__main__":
    # page_id = "Tripviss"
    # get_sentiment(page_id)
    get_sentiment_all_pages()