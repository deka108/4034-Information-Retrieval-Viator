from flask import Blueprint, jsonify

from server.core.crawler import crawler
from server import data_util

access_token = 'EAACEdEose0cBAP9s5lDmTubZAGr2KBKnAaQulX54mUvVV0mniQrhvbRDG3xcvzmsaMfMQFbkF2UFpluEX18kP7w5dgFjNjORmy7xJenpP8j4AbXZBD2DNfh4VsGTEgP0S5I5tChl7mY4UmtRt9pzvWBAyMEsz3LR63aTmscU0uVURQQUxIsO7a8lg77o5ZBHH5oyzif7wZDZD'

db_manager = Blueprint('db_manager', __name__, static_folder='static')

@db_manager.route('/crawl', methods=['POST'])
def crawl_all(data):
    try:
        # crawler.crawl_all(access_token)
        # return "success"
        return jsonify({
            "access_token": access_token
        })
    except:
        return "failure"


@db_manager.route('/crawl/<page_id>', methods=['POST'])
def crawl_specific(page_id):
    try:
        # crawler.crawl_page(page_id,access_token)
        # return "success"
        return jsonify({
            "page_id": page_id,
            "access_token": access_token
        })
    except Exception as e:
        print(e)
        return "fail"


@db_manager.route('/read', methods=['GET'])
def get_all_data():
    file_infos = data_util.get_all_json_info()
    if file_infos:
        return jsonify(file_infos)
    return "Data does not exist"


@db_manager.route('/read/<page_id>', methods=['GET'])
def read_data(page_id):
    file_name = data_util.get_json_filename(page_id)
    if file_name:
        return db_manager.send_static_file(file_name)
    return "Country does not exist"


@db_manager.route('/delete', methods=['DELETE'])
def delete_all_data():
    file_names = data_util.get_page_ids()
    if file_names:
        return jsonify(file_names)
    return "Data does not exist"


@db_manager.route('/delete/<page_id>', methods=['DELETE'])
def delete_data(page_id):
    file_name = data_util.get_json_filename(page_id)
    if file_name:
        return db_manager.send_static_file(file_name)
    return "Country does not exist"