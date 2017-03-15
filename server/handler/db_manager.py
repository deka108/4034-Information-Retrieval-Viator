import json

from flask import Blueprint, abort, jsonify, request
from flask import make_response

from server.utils import data_util
from server.core.solr import solr_interface

# access_token = 'EAACEdEose0cBAP9s5lDmTubZAGr2KBKnAaQulX54mUvVV0mniQrhvbRDG3xcvzmsaMfMQFbkF2UFpluEX18kP7w5dgFjNjORmy7xJenpP8j4AbXZBD2DNfh4VsGTEgP0S5I5tChl7mY4UmtRt9pzvWBAyMEsz3LR63aTmscU0uVURQQUxIsO7a8lg77o5ZBHH5oyzif7wZDZD'

db_manager = Blueprint('db_manager', __name__, static_folder='static')

@db_manager.route('/crawl/', methods=['POST'])
def crawl():
    try:
        request_data = json.loads(request.get_data())

        if request_data:
            page_id = request_data.get("page_id")
            access_token = request_data.get("token")

        # if access_token:
        #      if not page_id:
        #          crawler.crawl_all(access_token)
        #      else:
        #          crawler.crawl_page(page_id, access_token)

        return jsonify({
            "page_id": page_id,
            "access_token": access_token
        })
    except Exception as e:
        make_response(str(e), 404)


@db_manager.route('/records/', methods=['GET'])
def get_all_data():
    file_infos = data_util.get_records()
    if file_infos:
        return jsonify(file_infos)
    return make_response("Record does not exist", 404)


@db_manager.route('/read/', defaults={'page_id': None})
@db_manager.route('/read/<page_id>', methods=['GET'])
def read_data(page_id):
    if page_id:
        data = data_util.get_preprocessed_json_data_by_page_id(page_id)
        if data:
            return jsonify(data)
        return make_response("Page Id does not exist", 404)
    else:
        # not recommended, data is too big
        data = data_util.get_preprocessed_json_data_all()
        if data:
            return jsonify(data)
        return make_response("Unable to retrieve data", 404)


@db_manager.route('/delete/', methods=['DELETE'])
def delete_all_data():
    file_names = data_util.get_page_ids()
    if file_names:
        return jsonify(file_names)
    return make_response("Data does not exist", 404)


@db_manager.route('/delete/<page_id>', methods=['DELETE'])
def delete_data(page_id):
    file_name = data_util.get_page_json_filename(page_id)
    if file_name:
        return db_manager.send_static_file(file_name)
    return make_response("Page Id does not exist", 404)

