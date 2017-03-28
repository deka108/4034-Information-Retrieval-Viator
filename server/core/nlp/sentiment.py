from textblob import TextBlob
from server.utils import data_util
import pandas as pd
from guess_language import guess_language

csv_headers = ["comments_sentiment","comments_subjectivity",]
def get_sentiment(page_id):
    data= []
    counter = 0
    # df = data_util.get_csv_data(data_util.get_csv_data_by_pageid(page_id))
    df = data_util.get_csv_data_by_pageid(page_id)
    comments = df["comments"]
    for comment in comments:
        entry = {}
        sentiment = []
        subjectivity_list = []
        if type(comment) is not float:
            if(guess_language(comment) == 'en'):
                if (isinstance(comment, str)):
                    comment = comment.split(",")
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
                # data.append(ave_sentiment)
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
    filename = data_util.PAGE_CSV_FILE_NAME.format(page_id)
    # data_util.write_dict_to_csv(data, csv_headers, filename)
    df = pd.DataFrame(data)
    data_util.write_df_to_existing_csv(df,csv_headers,filename)

def get_sentiment_all_pages():
    all_pageids = data_util.get_page_ids()
    for page_id in all_pageids:
        get_sentiment(page_id)

if __name__ == "__main__":
    get_sentiment_all_pages()
    #all_posts = data_util.get_csv_data_all()
    #data_util.write_df_to_csv(all_posts, csv_headers, "all_posts")
