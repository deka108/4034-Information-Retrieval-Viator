import os

from flask import Flask
from .views.search import search_page
from .views.index import index_page
from .views.db_manager import db_manager

app = Flask(__name__)
app.config.from_pyfile('config.py')

# Registers Blueprints
app.register_blueprint(index_page, url_prefix='')
app.register_blueprint(search_page, url_prefix='/search')
app.register_blueprint(db_manager, url_prefix='/db')