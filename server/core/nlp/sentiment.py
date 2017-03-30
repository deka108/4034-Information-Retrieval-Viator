from textblob import TextBlob
from server.utils import data_util
import pandas as pd
from guess_language import guess_language

csv_headers = ["comments_sentiment","comments_subjectivity",]
def get_sentiment():
    page_id = data_util.ALL_POSTS_COMMENTS_FILENAME
    data= []
    counter = 0
    data_path = data_util.get_csv_filepath(page_id)
    df = data_util.get_csv_data(data_path)
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
    df = pd.DataFrame(data)
    file_name = data_util.ALL_POSTS_COMMENTS_FILENAME
    data_util.write_df_to_existing_csv(df,csv_headers,file_name)

def get_sentiment_all_pages():
    all_pageids = data_util.get_page_ids()
    for page_id in all_pageids:
        get_sentiment(page_id)

if __name__ == "__main__":
    get_sentiment()
