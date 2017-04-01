import json

import requests
from nltk.stem.porter import *

from server import config
from server.utils import data_util

s = requests.Session()
s.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
s.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))

stemmer = PorterStemmer()

def add_to_dict(posting):
    post_dict = {}
    try:
        post_dict['id'] = posting['id']
        
        try:
            post_dict['desc'] = posting['description']
            post_dict['descU'] = posting['description']
        except LookupError:
            print('no description in this post')

        try:
            post_dict['name'] = posting['name']
            post_dict['nameU'] = posting['name']
        except LookupError:
            print('no name in this post')

        try:
            post_dict['message'] = posting['message']
            post_dict['messageU'] = posting['message']
        except LookupError:
            print('no message in this post')

        try:
            post_dict['type'] = posting['type']
        except LookupError:
            print('no type in this post')

        try:
            post_dict['page_id'] = posting['page_id']
        except LookupError:
            print('no publisher in this post')

        try:
            post_dict['shares_count'] = posting['shares_cnt']
        except LookupError:
            print('no share count in this post')

        try:
            post_dict['reactions_count'] = posting['reactions_cnt']
        except LookupError:
            print('no reaction count in this post')

        try:
            post_dict['comments_count'] = posting['comments_cnt']
        except LookupError:
            print('no comment count in this post')

        try:
            post_dict['time'] = posting['updated_time']
        except LookupError:
            print('no update time in this post')

        try:
            post_dict['link'] = posting['link']
        except LookupError:
            print('no link in this post')

        try:
            post_dict['picture'] = posting['picture']
        except LookupError:
            print('no picture in this post')

        try:
            post_dict['full_picture'] = posting['full_picture']
        except LookupError:
            print('no full sized picture in this post')

        try:
            post_dict['day'] = posting['updated_day']
        except LookupError:
            print('no update day in this post')

        try:
            post_dict['month'] = posting['updated_month']
        except LookupError:
            print('no update month in this post')

        try:
            post_dict['year'] = posting['updated_year']
        except LookupError:
            print('no update year in this post')

        try:
            post_dict['is_weekend'] = posting['updated_is_weekend']
        except LookupError:
            print('no update time in this post')

        try:
            post_dict['comments_sentiment'] = posting['comments_sentiment']
        except LookupError:
            print('no comments\' sentiment in this post')

        try:
            post_dict['comments_subjectivity'] = posting['comments_subjectivity']
        except LookupError:
            print('no comments\' subjectivity in this post')

        return post_dict
    except LookupError:
        print('invalid post')
    


def send_to_solr(body_payload):
    print(json.dumps(body_payload))
    r = s.post("{url}/update".format(url=config.SOLR_BASE_URL),
                      headers={"Content-Type": "application/json"},
                      data=json.dumps(body_payload))
    print(r.json())


def delete_all_index():
    r = s.get("{url}/update?stream.body=<delete><query>*:*</query></delete>&commit=true".format(url=config.SOLR_BASE_URL))
    return r.status_code


def delete_index_by_page(page_id):
    r = s.get("{url}/update?stream.body=<delete><query>page_idss:{page_id}</query></delete>&commit=true".format(url=config.SOLR_BASE_URL, page_id=page_id))
    return r.status_code


def get_core():
    r = s.get("{url}/cores?action=STATUS&wt=json".format(url=config.SOLR_ADMIN_URL))
    return r.json()


def get_schema():
    r = s.get("{url}/schema".format(url=config.SOLR_BASE_URL))
    return r.json()


def index_specific(page_id):
    try:
        temp_json = data_util.get_preprocessed_json_data_by_page_id(page_id)
        if temp_json:
            for post in temp_json:
                to_be_posted = add_to_dict(post)

                payload = json.loads(''' {
                    "add": {"doc" : %s,
                    "commitWithin": 1000
                }}''' % json.dumps(to_be_posted))
                send_to_solr(payload)
            print("Successfully indexed {}".format(page_id))
        return True
    except:
        return False


def index_all():
    try:
        delete_all_index()
        page_ids = data_util.get_page_ids()
        for page_id in page_ids:
            index_specific(page_id)
        return True
    except:
        return False


def search(query, page, sort_by, order='ascending'):
    rows = 10
    try:
        page = int(page)
    except TypeError:
        page = 0

    start_num = rows*page
    payload = {'rows': rows,
               'start': start_num}
    payload['q'] = query
    if sort_by != 'relevance':
        if (sort_by == 'time') and (order == 'ascending'):
            payload['sort'] = 'time asc'
        elif (sort_by == 'time') and (order == 'descending'):
            payload['sort'] = 'time desc'
        elif (sort_by == 'reactions') and (order == 'ascending'):
            payload['sort'] = 'reactions_count asc'
        elif (sort_by == 'reactions') and (order == 'descending'):
            payload['sort'] = 'reactions_count desc'
        elif (sort_by == 'shares') and (order == 'ascending'):
            payload['sort'] = 'shares_count asc'
        elif (sort_by == 'shares') and (order == 'descending'):
            payload['sort'] = 'reactions_count desc'
    print(payload)
    r = s.get("{url}/query".format(url=config.SOLR_BASE_URL), params=payload)
    print(r.url)
    result_json = r.json()
    numFound = result_json['response']['numFound']
    result_json['next_page'] = bool(((page+1)*rows-numFound) < 0)

    query_bag = query.split()
    query_bag_stemmed = [stemmer.stem(query_unstemmed) for query_unstemmed in query_bag]
    pop_list = []

    for i in range(0, len(result_json['spellcheck']['suggestions']), 2):
        if result_json['spellcheck']['suggestions'][i] not in (query_bag + query_bag_stemmed):
            pop_list.append(i)

    while len(pop_list):
        delete_index = pop_list.pop()
        del result_json['spellcheck']['suggestions'][delete_index+1]
        del result_json['spellcheck']['suggestions'][delete_index]

    return result_json

def add_schema_field():
    return "Success"

def get_all_page_ids():
    r = s.get("{url}/select?q=*%3A*&rows=0&facet=on&facet.field=page_id&wt=json".format(url=config.SOLR_BASE_URL))
    return r.json()


def more_like_this(post_id):
    payload = {'q': 'id:{0}'.format(post_id),
               'mlt': 'true',
               'mlt.fl': 'mlt_field'}
    r = s.get("{url}/query".format(url=config.SOLR_BASE_URL), params=payload)
    return r.json()
    