from flask import Blueprint, jsonify

from server import config
from . import util
import requests

db_manager = Blueprint('db_manager', __name__, static_folder='../data')


@db_manager.route('/indexing/')
def indexing_all_database():
    countries = util.get_data_names()
    for country in countries:
        data = util.read_json_data(country)
        if data:
            try:
                r = requests.post(config.SOLR_UPDATE_JSON_URL, json=data)
                return "{} successfully indexed!".format(country)
            except requests.exceptions.ConnectionError: 
                return "Unable to connect with Solr server"
    return "Country not exist"


@db_manager.route('/indexing/<country>')
def indexing_country_database(country):
    data = util.read_json_data(country)
    if data:
        try:
            r = requests.post(config.SOLR_UPDATE_JSON_URL, json=data)
            return "{} successfully indexed!".format(country)
        except requests.exceptions.ConnectionError: 
            return "Unable to connect with Solr server"
    return "Country not exist"


@db_manager.route('/update/')
def update_database():
    return "send data to solr"


@db_manager.route('/delete/')
def delete_table():
    return "send data to solr"


@db_manager.route('/read/')
def get_all_data():
    file_names = util.get_data_names()
    if file_names:
        return jsonify(file_names)
    return "Data does not exist"


@db_manager.route('/read/<country>')
def read_data(country):
    file_name = util.get_file_name(country)
    if file_name:
        return db_manager.send_static_file(file_name)
    return "Country does not exist"


def reindex_database():
    pass