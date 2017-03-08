from flask import Blueprint, jsonify, request, abort

from server.core.solr import solr_interface

import json

search_page = Blueprint('search', __name__)

@search_page.route('/', methods=['POST'])
def search_query():
    query_params = {}

    request_data = json.loads(request.get_data())
    if request_data:
        query_params['q'] = request_data.get('q')
    
    query_params['hl'] = 'true'
    query_params['hl.fl'] = 'message_t'

    if 'q' in query_params:
        response = solr_interface.search(query_params)
        return jsonify(response)

    return abort(404)
