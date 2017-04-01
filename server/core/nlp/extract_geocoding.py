from server.utils import data_util
import pandas as pd
import geocoder


def extract_lat_long(location):
    return geocoder.arcgis(location)

def extract_unique_locations():
    pass


def get_all_locations():
    page_ids = data_util.get_page_ids()
    all_locations = []
    for page_id in page_ids:
        data_locations = data_util.get_csv_data_from_filename(
            page_id + "_locations")
        all_locations.append(data_locations["locations"])
    all_locations = pd.concat(all_locations)

    print(all_locations)

if __name__ == "__main__":
    # get_all_locations()
    print(extract_lat_long("Victoria Harbour"))