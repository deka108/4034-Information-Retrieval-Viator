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
        sort_params = request_data.get('s')
        order_params = request_data.get('o')
        filter = request_data.get('f')
        filter_query = request_data.get('fq')
        geoLocation = request_data.get('gl')
        
    response = solr_interface.search(query_params,page_params, sort_params, order_params, filter, filter_query, geoLocation)
    return jsonify(response)

    return abort(404)

@search_page.route('/more/', methods=['POST'])
def search_query_more():

    request_data = json.loads(request.get_data())
    if request_data:
        post_id = request_data.get('p')

    response = solr_interface.more_like_this(post_id)
    return jsonify(response)

    return abort(404)