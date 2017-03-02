from flask import Blueprint

from server.core.crawler import crawler
from server import util

access_token = 'EAACEdEose0cBAP9s5lDmTubZAGr2KBKnAaQulX54mUvVV0mniQrhvbRDG3xcvzmsaMfMQFbkF2UFpluEX18kP7w5dgFjNjORmy7xJenpP8j4AbXZBD2DNfh4VsGTEgP0S5I5tChl7mY4UmtRt9pzvWBAyMEsz3LR63aTmscU0uVURQQUxIsO7a8lg77o5ZBHH5oyzif7wZDZD'
crawl_page = Blueprint('crawl', __name__, static_folder='static')

@crawl_page.route('/')
def crawl_all():
    try:
        crawler.crawl_all(access_token)
        return "success"
    except:
        return "failure"

@crawl_page.route('/<page_id>')
def crawl_specific(page_id):
    try:
        #return util.get_json_file_path(page_id)
        crawler.crawl_page(page_id,access_token)
        return "success"
    except Exception as e:
        print(e)
        return "fail"
