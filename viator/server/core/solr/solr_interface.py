import json
import requests
from server import util, config


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


def test():
    # print(config.SOLR_BASE_URL)
    return util.read_json_data('china')


def delete_all_index():
    r = s.get("{url}/update?stream.body=<delete><query>*:*</query></delete>&commit=true".format(url=config.SOLR_BASE_URL))
    return str(r.status_code)


def delete_index_by_page(page_name):
    r = s.get("{url}/update?stream.body=<delete><query>page_name_s:{page_name}</query></delete>&commit=true".format(url=config.SOLR_BASE_URL, page_name=page_name))
    return str(r.status_code)


def get_core():
    r = s.get("{url}/cores?action=STATUS&wt=json".format(url=config.SOLR_ADMIN_URL))
    return r.json()

def get_schema():
    r = s.get("{url}/schema".format(url=config.SOLR_BASE_URL))
    return r.json()

def index_specific(country):
    temp_json = util.read_json_data(country)
    if temp_json:
        for branch in temp_json:
            for post in branch['data']:
                to_be_posted = add_to_dict(post)
                to_be_posted['page_name_s'] = country
                payload = json.loads(''' {
                    "add": {"doc" : %s,
                    "commitWithin": 1000
                }}''' % json.dumps(to_be_posted))
                send_to_solr(payload)
        return "Successfully indexed {}".format(country)
    return "Country does not exist"


def index_all():
    delete_all_index()
    data_names = util.get_data_names()
    for name in data_names:
        index_specific(name)
    return "Success"

def search(query_params):
    r = s.get("{url}/query/".format(url=config.SOLR_BASE_URL), params=query_params)
    return r.json()


def add_schema_field():
    return "Success"


