from flask import Blueprint
from .db_map import DATA_MAP

import requests

db_manager = Blueprint('db_manager', __name__, static_folder='../data')

@db_manager.route('/create')
def create_database():
    return "send data to solr"

@db_manager.route('/update')
def update_database():
    return "send data to solr"

@db_manager.route('/delete')
def delete_table():
    return "send data to solr"

@db_manager.route('/read/<country>')
def read_data(country):
    file_name = DATA_MAP.get(country)
    if file_name:
        return db_manager.send_static_file(file_name)
    return "Country not exist"

def reindex_database():
    pass