from flask import Blueprint

index_page = Blueprint('index', __name__, static_folder='static')

@index_page.route('/')
def index():
    return index_page.send_static_file('index.html')


@index_page.route('/<filename>')
def get_resource(filename):
    return index_page.send_static_file(filename)