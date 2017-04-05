import math
from requests import ReadTimeout

from server.utils import data_util
from server.core.nlp import location_ner_stanford as lns
import pandas as pd
import geocoder
import csv
import json
import re
import time
from pprint import pprint

NEW_LOCATION_CORPUS_FILENAME = "new_location_corpus.csv"
NEW_LOCATION_CORPUS_ALL_FILENAME = "new_location_corpus_all.csv"

LOCATION_CORPUS_ID_FILENAME = "location_corpus_{}.csv"
LOCATION_COLUMNS = ["location", "lat", "long", "post_ids"]
LOCATION_CORPUS = data_util.get_csv_data_from_filename(data_util.ALL_LOCATION_CORPUS)
LOCATION_CORPUS = LOCATION_CORPUS.fillna("")
LOCATION_CORPUS = LOCATION_CORPUS.set_index("location").to_dict(orient='index')


# read from corpus all
# update corpus
    # if do not exist there:
# update all
# reindex based on new locations


def extract_lat_long(location):
    return geocoder.arcgis(location).latlng


def extract_lat_long_row(row):
    res = []
    tries = 3
    running = True

    while running and tries > 0:
        try:
            res = extract_lat_long(row['location'])
            running = False
        except ReadTimeout:
            print("Retrying...")
            time.sleep(5)
            tries -= 1

    if len(res) == 2:
        row['lat'] = res[0]
        row['long'] = res[1]

    return row


def compile_lat_long():
    all_df = []
    for i in range(6):
        file_name = LOCATION_CORPUS_ID_FILENAME.format(i)
        df = pd.read_csv(file_name)
        all_df.append(df)
    all_df = pd.concat(all_df)
    all_df.to_csv(NEW_LOCATION_CORPUS_FILENAME, header=LOCATION_COLUMNS,
                  encoding='utf-8', index=False)


def update_location_corpus():
    all_locations = lns.get_all_locations()
    ordered_loc, new_location_data = get_new_locations(all_locations)
    n_split = split_locations(ordered_loc, new_location_data)
    for i in range(n_split):
        get_lat_long_id(i)
    # compile_lat_long()
    # combine with all corpus


def get_lat_long_id(id):
    file_name = LOCATION_CORPUS_ID_FILENAME.format(id)
    df = pd.read_csv(file_name)
    df.fillna("")
    df = df.apply(extract_lat_long_row, axis=1)
    df.to_csv(file_name, header=LOCATION_COLUMNS, encoding='utf-8',
              index=False)


def split_locations(ordered_loc, location_data):
    start = 0
    step = 1000
    end = len(ordered_loc)
    for i in range(start, end, step):
        if i + step - 1 < end:
            locs = ordered_loc[i:(i + step)]
        else:
            locs = ordered_loc[i:]

        with open(LOCATION_CORPUS_ID_FILENAME.format(int(i/1000)), "w") as fp:
            csvwriter = csv.writer(fp)
            csvwriter.writerow(LOCATION_COLUMNS)
            for loc in locs:
                csvwriter.writerow(
                    [loc, "", "", "$$".join(location_data[loc])])
    return math.ceil(end*1.0/(step - start))


def get_new_locations(locations):
    new_locations = {}

    for index, row in locations.iterrows():
        if pd.notnull(row["locations"]):
            locs = extract_locations(row["locations"])
            post_id = row["id"]
            for loc in locs:
                if loc not in LOCATION_CORPUS:
                    if loc in new_locations:
                        new_locations[loc].append(post_id)
                    else:
                        new_locations[loc] = [post_id]

    print(new_locations)

    with open(NEW_LOCATION_CORPUS_FILENAME, "w") as fp:
        csvwriter = csv.writer(fp)
        sort_locs = list(new_locations.keys())
        sort_locs.sort()
        csvwriter.writerow(LOCATION_COLUMNS)
        for loc in sort_locs:
            csvwriter.writerow([loc, "", "", "$$".join(new_locations[loc])])

    return sort_locs, new_locations


def extract_locations(locations):
    locs = locations.split("$$")
    locs = [loc.lower() for loc in locs]
    locs = [re.sub(r"[^a-z\s]", "", loc) for loc in locs]
    return locs


def get_all_locations():
    all_locations = data_util.get_csv_data_from_filename(
        data_util.ALL_POSTS_LOCATIONS_FILENAME)
    return all_locations


def add_coordinates(row):
    if pd.notnull(row["locations"]):
        locs = extract_locations(row["locations"])
        coords = []

        for loc in locs:
            if loc in LOCATION_CORPUS:
                lat = str(LOCATION_CORPUS[loc]["lat"])
                long = str(LOCATION_CORPUS[loc]["long"])
                coords.append(",".join([lat, long]))

        coords = "$$".join(coords)
        row["coords"] = coords
    else:
        row["coords"] = ""
    return row


def extract_new_coordinates(row):
    if pd.notnull(row["locations"]):
        locs = extract_locations(row["locations"])
        coords = []

        for loc in locs:
            if loc in LOCATION_CORPUS:
                lat = str(LOCATION_CORPUS[loc]["lat"])
                long = str(LOCATION_CORPUS[loc]["long"])
                coords.append(",".join([lat, long]))

        coords = "$$".join(coords)
        row["coords"] = coords
    else:
        row["coords"] = ""
    return row


def add_locations_to_posts():
    page_ids = data_util.get_page_ids()

    for page_id in page_ids:
        data = data_util.get_csv_data_by_pageid(page_id)
        data_locations = data_util.get_csv_data_from_filename(
            page_id + "_locations")
        data_locations = data_locations.apply(add_coordinates, axis=1)
        filtered_loc = data_locations[["id", "locations", "coords"]]
        combined = pd.merge(data, filtered_loc, on="id")

        data_util.write_df_to_csv(combined, combined.columns,
                                  data_util.get_page_csv_filename(page_id))


def add_locations_to_all_posts():
    page_ids = data_util.get_page_ids()
    print("Adding locations to all page ids...")
    for page_id in page_ids:
        add_locations_to_pageid(page_id)
    print("Locations added to all page ids!")


def add_locations_to_pageid(page_id):
    print("Adding locations to page:{}...".format(page_id))
    location_data = data_util.get_csv_data_from_filename(
        data_util.PAGE_LOCATION_FILENAME.format(page_id))
    location_data = location_data.apply(extract_new_coordinates, axis=1)
    data = data_util.get_csv_data_by_pageid(page_id)
    filtered_loc = location_data[["id", "locations", "coords"]]
    combined = pd.merge(data, filtered_loc, on="id")
    data_util.write_df_to_csv(combined, combined.columns,
                              data_util.get_csv_data_by_pageid(page_id))
    print("Locations added to page:{}...".format(page_id))


def run():
    add_locations_to_posts()

if __name__ == "__main__":
    # build_location_corpus()
    # CHANGE ID!!!!
    #get_lat_long_id(4)
    # compile_lat_long()
    # get_lat_long_id()
    # compile_lat_long()
    run()
    # add_locations_to_pageid("Tripviss")
    # pprint(LOCATION_CORPUS)
    # update_location_corpus()

