import pandas as pd

from server.utils import data_util, text_util
from guess_language import guess_language

csv_headers = [
    # content
    "id", "page_id", "type", "name", "message", "link", "caption", "picture",
    "description","full_picture", "story",
    # user preference
    "likes_cnt", "shares_cnt", "reactions_cnt", "comments_cnt", "comments",
    # location
    "loc_city", "loc_country", "loc_lat", "loc_long", "loc_street", "loc_zip",
    # Time info
    "created_time", "created_year", "created_month", "created_day",
    "created_is_weekend",
    "updated_time", "updated_year", "updated_month", "updated_day",
    "updated_is_weekend",]


def preprocess_all_pages():
    all_pageids = data_util.get_page_ids()
    for page_id in all_pageids:
        preprocess_page_json(page_id)
    all_posts = data_util.get_csv_data_all()
    data_util.write_df_to_csv(all_posts, csv_headers, data_util.ALL_POSTS_FILENAME)
    # generate_all_posts_with_comment()


#Clean all post without message or description
def preprocess_page_json(page_id):
    postdata = data_util.get_raw_json_data_by_page_id(page_id)
    data = []
    #i = 0

    #ave_sentiment = sentiment.get_sentiment(page_id)
    # must extract data
    for post in postdata:
        entry = {}
        if post.get("message") and (len((post.get("message")).split(" ")))>3 or post.get("description") and (len((post.get("description")).split(" ")))>3:
            text_content = post.get("message", "") + " " + post.get(
                "description", "")
            if guess_language(text_content) == "en":
                # CONTENT
                # must be available
                entry["page_id"] = page_id
                entry["id"] = post["id"]
                entry["type"] = post["type"]

                # might be available
                entry["link"] = post.get("link")

                # might be available and unicode
                entry["name"] = post.get("name", "").encode('utf-8').decode('utf-8', 'ignore')
                entry["message"] = post.get("message", "").encode('utf-8').decode('utf-8', 'ignore')
                entry["caption"] = post.get("caption", "").encode('utf-8').decode('utf-8', 'ignore')
                entry["picture"] = post.get("picture", "").encode('utf-8').decode('utf-8', 'ignore')
                entry["full_picture"] = post.get("full_picture", "").encode('utf-8').decode('utf-8', 'ignore')
                entry["description"] = post.get("description", "").encode('utf-8').decode('utf-8', 'ignore')
                entry["story"] = post.get("story", "").encode('utf-8').decode('utf-8', 'ignore')

                if "likes" in post:
                    entry["likes_cnt"] = int(post["likes"]["summary"].get("total_count",0))
                else:
                    entry["likes_cnt"] = 0
                if "reactions" in post:
                    entry["reactions_cnt"] = int(post["reactions"]["summary"].get("total_count",0))
                else:
                    entry["reactions_cnt"] = 0
                if "shares" in post:
                    entry["shares_cnt"] = int(post["shares"]["count"])
                else:
                    entry["shares_cnt"] = 0
                if "comments" in post:
                    entry["comments_cnt"] = int(post["comments"]["summary"].get("total_count",0))
                    comment_data = post["comments"]["data"]
                    message_list = []
                    for message in comment_data:
                        #print(message["message"])
                        if type(message["message"]) is str:
                            if(guess_language(message["message"]) == 'en'):
                                message_list.append(message["message"])
                    entry["comments"] = '$$'.join(message_list)
                    #entry["comments_sentiment"] = ave_sentiment[i]
                    #i += 1
                else:
                    entry["comments_cnt"] = 0
                    entry["comments"] = ""
                    # entry["comments_sentiment"] = 0

                # LOCATION
                if "place" in post:
                    entry["loc_city"] = post["place"].get("city")
                    entry["loc_country"] = post["place"].get("country")
                    entry["loc_lat"] = post["place"].get("latitude")
                    entry["loc_long"] = post["place"].get("longitude")
                    entry["loc_street"] = post["place"].get("street")
                    entry["loc_zip"] = post["place"].get("zip")

                # DATE TIME INFO
                entry["created_time"] = post["created_time"]
                entry["created_year"], entry["created_month"], entry["created_day"], \
                entry["created_is_weekend"] = text_util.extract_date(post["created_time"])

                entry["updated_time"] = post["updated_time"]
                entry["updated_year"], entry["updated_month"], entry["updated_day"], \
                entry["updated_is_weekend"] = text_util.extract_date(post["updated_time"])

                if len(entry['comments']) > 0:
                    entry['comments'] = entry['comments'].encode('utf-8').decode('utf-8', 'ignore')
                    data.append(entry)

    file_name = data_util.PAGE_CSV_FILENAME.format(page_id)
    data_util.write_dict_to_csv(data, csv_headers, file_name)
    print("Successfully written preprocessed data to {}.csv".format(file_name))


def compute_words(df):
    df["message_cleaned"] = df["message"].apply(
        lambda x: text_util.clean_text(x) if pd.notnull(x) else "")
    # print(df["message_cleaned"])
    text_util.count_words(df["message_cleaned"])


def read_csv_by_pageid(page_id):
    df = data_util.get_csv_data_from_path(page_id)
    print(df)
    return df


def generate_all_posts_with_comment():
    df = data_util.get_csv_data_from_filename(data_util.ALL_POSTS_FILENAME)
    df = df[pd.notnull(df.comments)]
    data_util.write_df_to_csv(df, csv_headers, data_util.ALL_POSTS_COMMENTS_FILENAME)

if __name__ == "__main__":
    preprocess_all_pages()
    #generate_all_posts_with_comment()
    # generate_all_posts_with_comment()

    # all_posts = data_util.get_csv_data_all()
    # data_util.write_df_to_csv(all_posts, csv_headers, "all_posts")

    # Example proccessing one page_id
    # page_id = "Tripviss"
    # preprocess_page_json(page_id)
    # compute_words(page_id)

    # get all preprocessed page data in 1 dataframe:
    # data = data_util.get_all_posts()
    # compute_words(data)