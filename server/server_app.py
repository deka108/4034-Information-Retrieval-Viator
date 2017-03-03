import os

from flask_api import FlaskAPI
from .handler.search import search_page
from .handler.index import index_page
from .handler.solr_manager import solr_manager
from .handler.db_manager import db_manager

app = FlaskAPI(__name__)
app.config.from_pyfile('config.py')

# Registers Blueprints
app.register_blueprint(index_page, url_prefix='')
app.register_blueprint(search_page, url_prefix='/search')
app.register_blueprint(db_manager, url_prefix='/db')
app.register_blueprint(solr_manager, url_prefix='/solr')
