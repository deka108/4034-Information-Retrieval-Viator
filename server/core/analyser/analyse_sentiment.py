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
    df_all.to_csv("file.csv")
    # s
    # print(sentiment_list)
    # file_name = data_util.PAGE_CSV_FILENAME.format("Results")
    # data_util.write_dict_to_csv(sentiment_list,csv_headers,file_name)



if __name__ == "__main__":
    # page_id = "indonesia.travel"
    combine_all_sentiment()