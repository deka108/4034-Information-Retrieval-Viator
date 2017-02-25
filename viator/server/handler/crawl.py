from flask import Blueprint

from server.core.crawler import crawler

crawl_page = Blueprint('crawl', __name__, static_folder='static')

@crawl_page.route('/')
def crawl_main():
    try:
        crawler.crawl_main()
        return "success"
    except:
        return "failure"