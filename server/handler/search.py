from flask import Blueprint, jsonify, request

from server.core.solr import solr_interface

import json

search_page = Blueprint('search', __name__)

@search_page.route('/', methods=['POST'])
def search_query():
    query_params = {}

    query_params['q'] = request.json[u'query']
    query_params['hl'] = 'true'
    query_params['hl.fl'] = 'message_t'

    response = solr_interface.search(query_params)

    return jsonify(response)

class SearchResult(object):

    def __init__(self, result):
        pass
        # self.url = result['url']
        # self.title_text = result['title']
        # self.title = highlight_all(result, 'title')
        # cls = import_string(result['type'])
        # self.kind = cls.search_document_kind
        # self.description = cls.describe_search_result(result)
    

class SearchResultPage(object):

    def __init__(self, results, page):
        # self.page = page
        # if results is None:
        #     self.results = []
        #     self.pages = 1
        #     self.total = 0
        # else:
        #     self.results = [SearchResult(r) for r in results]
        #     self.pages = results.pagecount
        #     self.total = results.total
        pass

    def __iter__(self):
        # return iter(self.results)
        pass

def search(query):
    pass
