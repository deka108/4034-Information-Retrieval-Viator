from flask import Blueprint

index_page = Blueprint('index', __name__, static_folder='static')

@index_page.route('/')
def index():
    return index_page.send_static_file('index.html')


