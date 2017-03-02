from flask import Blueprint

from server.core.crawler import crawler

access_token = 'EAACEdEose0cBAIVoIaZAajt0ZBAVZBLE9Gl4cxJhDSXh1r7WqDN6lut0UiEpHMbJdytQnMpUaNoKuXpnXFa2nidNvkP3xkwmsAywdcXxxgySsyhH3VQwGTapY8lSL4B9tda2bT4jutbkl9L0d5GedCavVLdaZA6SZCaTa4zHhqjMrt3Pk4KTuZB3SyZAAHhK0ZAfDtkjfRLT4gZDZD'
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
        crawler.crawl_data(page_id,access_token)
        return "success"
    except:
        return "failure"
