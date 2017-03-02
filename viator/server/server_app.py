import os

from flask import Flask
from .handler.search import search_page
from .handler.index import index_page
from .handler.db_manager import db_manager
from .handler.crawl import crawl_page

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Registers Blueprints
app.register_blueprint(index_page, url_prefix='')
app.register_blueprint(search_page, url_prefix='/search')
app.register_blueprint(db_manager, url_prefix='/db')
app.register_blueprint(crawl_page, url_prefix='/crawler')
