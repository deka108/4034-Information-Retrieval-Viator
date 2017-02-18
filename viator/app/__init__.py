import os

from flask import Flask
from views.search import search_page
from views.index import index_page

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    # Registers Blueprints
    app.register_blueprint(search_page)
    app.register_blueprint(index_page)

    return app