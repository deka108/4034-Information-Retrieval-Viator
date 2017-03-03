import json
import requests
from server import data_util, config


s = requests.Session()
s.mount('http://', requests.adapters.HTTPAdapter(max_retries=5))
s.mount('https://', requests.adapters.HTTPAdapter(max_retries=5))


def add_to_dict(posting):
    post_dict = {}
    try:
        post_dict['id'] = posting['id']

        try:
            post_dict['name_t'] = posting['name']
        except LookupError:
            print('no name in this post')

        try:
            post_dict['message_t'] = posting['message']
        except LookupError:
            print('no message in this post')

        try:
            post_dict['type_s'] = posting['type']
        except LookupError:
            print('no type in this post')

        try:
            post_dict['from_s'] = posting['from']['name']
        except LookupError:
            print('no publisher in this post')

        try:
            post_dict['share_count_i'] = posting['shares']['count']
        except LookupError:
            print('no share count in this post')

        try:
            post_dict['time_dt'] = posting['updated_time']
        except LookupError:
            print('no update time in this post')

        try:
            post_dict['desc_t'] = posting['description']
        except LookupError:
            print('no description in this post')

    except LookupError:
        print('invalid post')
    return post_dict


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
    r = s.get("{url}/update?stream.body=<delete><query>page_id_s:{page_id}</query></delete>&commit=true".format(url=config.SOLR_BASE_URL, page_id=page_id))
    return r.status_code


def get_core():
    r = s.get("{url}/cores?action=STATUS&wt=json".format(url=config.SOLR_ADMIN_URL))
    return r.json()


def get_schema():
    r = s.get("{url}/schema".format(url=config.SOLR_BASE_URL))
    return r.json()


def index_specific(page_id):
    temp_json = data_util.get_json_data_by_page_id(page_id)
    if temp_json:
        for post in temp_json:
            to_be_posted = add_to_dict(post)
            to_be_posted['page_id_s'] = page_id

            payload = json.loads(''' {
                "add": {"doc" : %s,
                "commitWithin": 1000
            }}''' % json.dumps(to_be_posted))
            send_to_solr(payload)
        return "Successfully indexed {}".format(page_id)
    return "Page ID does not exist"


def index_all():
    delete_all_index()
    page_ids = data_util.get_page_ids()
    for page_id in page_ids:
        index_specific(page_id)
    return "Success"


def search(query_params):
    r = s.get("{url}/query/".format(url=config.SOLR_BASE_URL), params=query_params)
    return r.json()


def add_schema_field():
    return "Success"


def get_all_page_ids():
    r = s.get("{url}/select?q=*:*&rows=0&facet=on&facet.field=page_id_s".format(url=config.SOLR_BASE_URL))
    return r.json()


