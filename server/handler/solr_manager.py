from flask import Blueprint, abort, jsonify, make_response, request

from server.core.solr import solr_interface

solr_manager = Blueprint('solr_manager', __name__, static_folder='../data')


@solr_manager.route('/delete/', methods=['DELETE'])
def delete_table():
    status_code = solr_interface.delete_all_index()
    if status_code < 400:
        return make_response(jsonify(success=True), status_code)
    abort(status_code)


@solr_manager.route('/delete/<page_id>', methods=['DELETE'])
def delete_table_name(page_id):
    status_code = solr_interface.delete_index_by_page(page_id)
    if status_code < 400:
        return make_response(jsonify(success=True), status_code)
    abort(status_code)


@solr_manager.route('/read/', methods=['GET'])
def get_all_index_data():
    return jsonify(solr_interface.get_all_page_ids())


@solr_manager.route('/core/', methods=['GET'])
def get_core():
    return jsonify(solr_interface.get_core())


@solr_manager.route('/schema', defaults={'path': ''})
@solr_manager.route('/schema/<path:path>')
def get_schema(path):
    return jsonify(solr_interface.get_schema())


@solr_manager.route('/indexing/', defaults={'page_id': None})
@solr_manager.route('/indexing/<page_id>', methods=['GET'])
def index_data(page_id):
    if page_id:
        if solr_interface.index_specific(page_id):
            return "Success indexed {}".format(page_id)
        return make_response("Page Id does not exist", 404)
    else:
        solr_interface.index_all()
        return "Success"


@solr_manager.route('/query/', methods=['GET'])
def get_query():
    query = request.args.get('q')
    return jsonify(solr_interface.search(query))
