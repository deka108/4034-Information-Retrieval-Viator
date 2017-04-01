from server.utils import data_util
import pandas as pd
import geocoder
import csv
import json
import re

LOCATION_CORPUS_ID_FILENAME = "location_corpus_{}.csv"
LOCATION_COLUMNS = ["location", "lat", "long", "post_ids"]


def extract_lat_long(location):
    return geocoder.arcgis(location).latlng


def extract_lat_long_row(row):
    res = extract_lat_long(row['location'])
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
    all_df.to_csv("location_corpus_all.csv", header=LOCATION_COLUMNS,
                  encoding='utf-8', index=False)


def build_location_corpus():
    all_locations = get_all_locations()
    ordered_loc, location_data = get_unique_locations(all_locations)
    split_locations(ordered_loc, location_data)


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


def get_unique_locations(locations):
    unique_locations = {}

    for index, row in locations.iterrows():
        if pd.notnull(row["locations"]):
            locs = row["locations"].split("$$")
            locs = [loc.lower() for loc in locs]
            locs = [re.sub(r"[^a-z\s]", "", loc) for loc in locs]
            post_id = row["id"]
            for loc in locs:
                if loc in unique_locations:
                    unique_locations[loc].append(post_id)
                else:
                    unique_locations[loc] = [post_id]

    print(unique_locations)

    with open("location_corpus.json", "w") as fp:
        json.dump(unique_locations, fp, sort_keys=True, indent=2)

    with open("location_corpus.csv", "w") as fp:
        csvwriter = csv.writer(fp)
        sort_locs = list(unique_locations.keys())
        sort_locs.sort()
        csvwriter.writerow(LOCATION_COLUMNS)
        for loc in sort_locs:
            csvwriter.writerow([loc, "", "", "$$".join(unique_locations[loc])])

    return sort_locs, unique_locations


def get_all_locations():
    page_ids = data_util.get_page_ids()
    all_locations = []
    for page_id in page_ids:
        data_locations = data_util.get_csv_data_from_filename(
            page_id + "_locations")
        all_locations.append(data_locations)
    all_locations = pd.concat(all_locations)
    return all_locations


if __name__ == "__main__":
    # build_location_corpus()
    # CHANGE ID!!!!
    get_lat_long_id(6)
    # compile_lat_long()