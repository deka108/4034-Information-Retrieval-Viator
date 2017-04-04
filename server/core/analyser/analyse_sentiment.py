import pandas as pd
from server.utils import data_util
import csv

csv_headers = ["id","comments_sentiment"]
def combine_all_sentiment():
    sentiment_list = []
    all_pageids = data_util.get_page_ids()
    for page_id in all_pageids:
        df = pd.read_csv(data_util.get_csv_filepath(data_util.get_page_csv_filename(page_id)))
        sentiment_list.append(df["comments_sentiment"])
    # print(sentiment_list)
    df_all = pd.concat(sentiment_list)
    df_all.to_csv("sentiment_analysis.csv")
    # s
    # print(sentiment_list)
    # file_name = data_util.PAGE_CSV_FILENAME.format("Results")
    # data_util.write_dict_to_csv(sentiment_list,csv_headers,file_name)

def analyze_popularity():
    df = data_util.get_csv_data_from_filename(data_util.ALL_POSTS_FILENAME)
    df["popularity"] = df["comments_cnt"] + df["shares_cnt"] + df["reactions_cnt"]
    df["popularity"].to_csv("popularity_analysis.csv", index=False)



if __name__ == "__main__":
    # page_id = "indonesia.travel"
    # combine_all_sentiment()
    analyze_popularity()