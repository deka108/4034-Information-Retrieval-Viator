import csv
import math
import re
import time

import geocoder
import pandas as pd
from requests import ReadTimeout

from server.core.nlp import location_ner_stanford as lns
from server.utils import data_util
from server.utils.data_util import NEW_LOCATION_CORPUS_FILENAME, \
    SPLIT_LOCATION_CORPUS_FILENAME, ALL_LOCATION_CORPUS_FILENAME

LOCATION_COLUMNS = ["location", "lat", "long", "post_ids"]
LOCATION_CORPUS = data_util.get_csv_data_from_filename(
    ALL_LOCATION_CORPUS_FILENAME)
LOCATION_CORPUS = LOCATION_CORPUS.fillna("")
LOCATION_CORPUS = LOCATION_CORPUS.set_index("location").to_dict(orient='index')

# Pipeline:
# 0: Extract NER of all posts (done by location_ner_stanford module)
# 1: Update location corpus
# 2: Add locations to all posts using the updated location corpus


def update_location_corpus():
    """1. Update Location corpus: extract the coordinates for new locations"""
    # Get all location NER from all posts (already done)
    all_locations = lns.get_all_locations()

    # Extract new locations from all posts
    ordered_loc, new_location_data = get_new_locations(all_locations)

    # Split new locations to 1000 due to the rate limit of the geocoding API
    n_split = split_locations(ordered_loc, new_location_data)
    if n_split > 0:
        for i in range(n_split):
            # Extract coordinates
            get_lat_long(i)

        # Compile splitted new coordinates
        new_locations = compile_new_lat_long(n_split)

        # Update the existing corpus with new coordinates
        compile_all_corpus(new_locations)


def get_new_locations(all_locations):
    """1.a. Get new locations ie. does not exist in the location corpus"""
    new_locations = {}

    for index, row in all_locations.iterrows():
        if pd.notnull(row["locations"]):
            locs = extract_locations(row["locations"])
            post_id = row["id"]
            for loc in locs:
                # Add new if the loc does not exist in location corpus
                if loc not in LOCATION_CORPUS:
                    if loc in new_locations:
                        new_locations[loc].append(post_id)
                    else:
                        new_locations[loc] = [post_id]

    print(new_locations)

    csv_path = data_util.get_csv_filepath(NEW_LOCATION_CORPUS_FILENAME)
    with open(csv_path, "w") as fp:
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


def split_locations(ordered_loc, location_data):
    """1.b. Split new locations into 1000 chunks"""
    start = 0
    step = 1000
    end = len(ordered_loc)
    for i in range(start, end, step):
        if i + step - 1 < end:
            locs = ordered_loc[i:(i + step)]
        else:
            locs = ordered_loc[i:]

        file_name = SPLIT_LOCATION_CORPUS_FILENAME.format(int(i / 1000))
        csv_path = data_util.get_csv_filepath(file_name)
        with open(csv_path, "w") as fp:
            csvwriter = csv.writer(fp)
            csvwriter.writerow(LOCATION_COLUMNS)
            for loc in locs:
                csvwriter.writerow(
                    [loc, "", "", "$$".join(location_data[loc])])
    return math.ceil(end*1.0/(step - start))


def get_lat_long(split_id):
    """1.c. Extract coordinates for the new location corpus"""
    file_name = SPLIT_LOCATION_CORPUS_FILENAME.format(split_id)
    df = data_util.get_csv_data_from_filename(file_name)
    df.fillna("")
    df = df.apply(extract_lat_long_row, axis=1)
    data_util.write_df_to_csv(df, LOCATION_COLUMNS, file_name)


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


def compile_new_lat_long(n):
    """1.d. Compile the splitted new coordinates"""
    all_df = []
    for i in range(n):
        file_name = SPLIT_LOCATION_CORPUS_FILENAME.format(i)
        df = data_util.get_csv_data_from_filename(file_name)
        all_df.append(df)
    all_df = pd.concat(all_df)
    data_util.write_df_to_csv(all_df, LOCATION_COLUMNS,
                              NEW_LOCATION_CORPUS_FILENAME)
    return all_df


def compile_all_corpus(new_locations):
    """1.e. Update the existing location corpus with the new coordinates"""
    LOCATION_CORPUS.append(new_locations)
    LOCATION_CORPUS.sort(['location'], inplace=True)
    data_util.write_df_to_csv(LOCATION_CORPUS, LOCATION_CORPUS.columns,
                              ALL_LOCATION_CORPUS_FILENAME)


def add_locations_to_all_posts():
    """2. Add coordinates to all posts"""
    page_ids = data_util.get_page_ids()
    print("Adding locations to all page ids...")
    for page_id in page_ids:
        add_locations_to_pageid(page_id)


def add_locations_to_pageid(page_id):
    print("Adding locations to page:{}...".format(page_id))
    data = data_util.get_csv_data_by_pageid(page_id)
    location_data = data_util.get_csv_data_from_filename(
        data_util.PAGE_LOCATION_FILENAME.format(page_id))
    location_data = location_data.apply(extract_coordinates, axis=1)

    if "locations" in data:
        data.drop("locations", axis=1, inplace=True)
    if "coords" in data:
        data.drop("coords", axis=1, inplace=True)

    filtered_loc = location_data[["id", "locations", "coords"]]
    combined = pd.merge(data, filtered_loc, on="id")
    data_util.write_df_to_csv(combined, combined.columns,
                              data_util.get_page_csv_filename(page_id))
    print("Locations added to page:{}...".format(page_id))


def extract_coordinates(row):
    """2.a. Extract coordinates from location corpus"""
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


def run():
    update_location_corpus()
    add_locations_to_all_posts()


def run_pageid(page_id):
    update_location_corpus()
    add_locations_to_pageid(page_id)


if __name__ == "__main__":
    # update corpus
    # read from corpus all
    # not in location corpus: add to new location
    # update all
    # reindex based on new locations

    # build_location_corpus()
    # CHANGE ID!!!!
    # get_lat_long_id(4)
    # compile_lat_long()
    # get_lat_long_id()
    # compile_lat_long()
    # add_locations_to_pageid("Tripviss")
    # pprint(LOCATION_CORPUS)
    # update_location_corpus()
    pass

    # run()