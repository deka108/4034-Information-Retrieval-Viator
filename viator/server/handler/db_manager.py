import requests

from flask import Blueprint, jsonify

from server.core.solr import solr_interface
from server import config, util


db_manager = Blueprint('db_manager', __name__, static_folder='../data')


@db_manager.route('/indexing/')
def indexing_all_database():
    return solr_interface.index_all()


@db_manager.route('/indexing/<country>')
def indexing_country_database(country):
    return solr_interface.index_specific(country)


@db_manager.route('/delete/')
def delete_table():
    return solr_interface.delete_all_index()


@db_manager.route('/delete/<country>')
def delete_table_name(country):
    return solr_interface.delete_index_by_page(country)


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


@db_manager.route('/core')
def get_core():
    return jsonify(solr_interface.get_core())


@db_manager.route('/schema', defaults={'path': ''})
@db_manager.route('/schema/<path:path>')
def get_schema(path):
    return jsonify(solr_interface.get_schema())