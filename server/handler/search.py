from flask import Blueprint, jsonify, request, abort

from server.core.solr import solr_interface

import json

search_page = Blueprint('search', __name__)

@search_page.route('/', methods=['POST'])
def search_query():

    request_data = json.loads(request.get_data())
    if request_data:
        query_params = request_data.get('q')
        page_params = request_data.get('p')

    response = solr_interface.search(query_params,page_params)
    return jsonify(response)

    return abort(404)
