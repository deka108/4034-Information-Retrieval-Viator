from textblob import TextBlob
from server.utils import data_util
import pandas as pd

csv_headers = ["comments_sentiment",]
def get_sentiment(page_id):
    data= []
    counter = 0
    # df = data_util.get_csv_data(data_util.get_csv_data_by_pageid(page_id))
    df = data_util.get_csv_data_by_pageid(page_id)
    comments = df["comments"]
    for comment in comments:
        entry = {}
        sentiment =[]
        subjectivity=[]
        if (isinstance(comment, str)):
            comment = comment.split(",")
        else:
            comment = " "
        for sentence in comment:
            comment_data = TextBlob(sentence)
            polarity = comment_data.sentiment.polarity
            subjectivity = comment_data.subjectivity
            #print(subjectivity)
            sentiment.append(polarity)
        ave_sentiment = sum(sentiment)/(len(sentiment))
        # data.append(ave_sentiment)
        counter += 1
        entry["comments_sentiment"] = ave_sentiment
        data.append(entry)
    print(counter)
    # print(data)
    #return data
    filename = data_util.PAGE_CSV_FILE_NAME.format(page_id)
    # data_util.write_dict_to_csv(data, csv_headers, filename)
    df = pd.DataFrame(data)
    data_util.write_df_to_existing_csv(df,csv_headers,filename)
    
if __name__ == "__main__":
     page_id = "Tripviss"
     get_sentiment(page_id)
