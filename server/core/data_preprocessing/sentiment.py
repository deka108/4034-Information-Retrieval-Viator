from textblob import TextBlob
from server.utils import data_util, text_util

def get_sentiment(page_id):
    data= []
    counter = 0
    df = data_util.get_csv_data(data_util.get_page_csv_filename(page_id))
    comments = df["comments"]

    for comment in comments:
        sentiment =[]
        if (isinstance(comment, str)):
            comment = comment.split(",")
        else:
            comment = " "
        for sentence in comment:
            comment_data = TextBlob(sentence)
            polarity = comment_data.sentiment.polarity
            sentiment.append(polarity)
        ave_sentiment = sum(sentiment)/(len(sentiment))
        data.append(ave_sentiment)
        counter += 1
    print (counter)
    return data


if __name__ == "__main__":
     page_id = "Tripviss"
     get_sentiment(page_id)
