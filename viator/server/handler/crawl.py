from flask import Blueprint

from server.core.crawler import crawler
from server import util

access_token = 'EAACEdEose0cBAG45hxAvpUUaPOFdmAA85DmZAYPwdMIB5vC7SmS57fsare9iABpdy1pNTU85SzF8vwX4A2kdvS1abA8AXAvQh2RQvNZBUEToJz6ZBVMlZARcTFQ3GamcdgKfOi4Wzw7Cbv1yR1vZBroMK46NofxWRAsNA5Y8ArnM1CNxQbWKx6vfTgSxS9OkZD'
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
