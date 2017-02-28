from server import config
import json

DATA_MAP = {
    'hongkong' : 'DiscoverHongKong_facebook.json',
    'turkey' : 'goturkeytourism_facebook.json',
    'india': 'incredibleindia_facebook.json',
    'indonesia.travel': 'indonesia.travel_facebook.json',
    'indonesiatravel': 'indonesiatravel_facebook.json',
    'philipphines': 'itsmorefuninthePhilippines_facebook.json',
    'korea': 'koreatourism_facebook.json',
    'malaysia': 'malaysia.travel.sg_facebook.json',
    'singapore': 'TheSmartLocal_facebook.json',
    'tripadvisor': 'TripAdvisor_facebook.json',
    'tripviss': 'Tripviss_facebook.json',
    'china': 'visitchinanow_facebook.json',
    'japan': 'visitjapaninternational_facebook.json',
    'indonesia': 'wonderfulplacesindo_facebook.json'
}


def get_data_names():
    return DATA_MAP.keys()

def get_file_path(country):
    if country in DATA_MAP:
        return config.get_data_path(DATA_MAP[country])

def get_file_name(country):
    if country in DATA_MAP:
        return DATA_MAP[country]

def read_json_data(country):
    data_path = get_file_path(country)
    if data_path:
        with open(data_path) as data_file:
            return json.load(data_file)