from server.utils import data_util, text_util
import pandas as pd

# Headers are ordered
csv_headers = [
    # content
    "id", "type", "name", "message", "link", "caption", "picture",
    # user preference
    "likes_cnt", "shares_cnt", "reactions_cnt", "comments_cnt",
    "comments_sentiment",
    # location
    "loc_city", "loc_country", "loc_lat", "loc_long", "loc_street", "loc_zip",
    # Time info
    "created_time", "created_year", "created_month", "created_day",
    "created_is_weekend",
    "updated_time", "updated_year", "updated_month", "updated_day",
    "updated_is_weekend"]


def preprocess_page_json(page_id):
    postdata = data_util.get_json_data_by_page_id(page_id)
    data = []

    # must extract data
    for post in postdata:
        entry = {}

        # CONTENT
        # must be available
        entry["id"] = post["id"]
        entry["type"] = post["type"]
        entry["link"] = post["link"]

        # might be available
        entry["name"] = post.get("name")
        entry["message"] = post.get("message")
        entry["caption"] = post.get("caption")
        entry["picture"] = post.get("picture")

        if "likes" in post:
            entry["likes_cnt"] = int(post["likes"]["summary"]["total_count"])
        if "reactions" in post:
            entry["reactions_cnt"] = int(post["reactions"]["summary"][
                "total_count"])
        if "shares" in post:
            entry["shares_cnt"] = int(post["shares"]["count"])
        else:
            entry["shares_cnt"] = 0

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

        data.append(entry)

    data_util.write_dict_to_csv(data, csv_headers, page_id)


def compute_words(page_id):
    df = read_csv_by_pageid(page_id)
    df["message_cleaned"] = df["message"].apply(
        lambda x: text_util.clean_text(x) if pd.notnull(x) else "")
    # print(df["message_cleaned"])
    text_util.count_words(df["message_cleaned"])


def read_csv_by_pageid(page_id):
    df = data_util.get_csv_data_by_page_id(page_id)
    # print(df)
    return df