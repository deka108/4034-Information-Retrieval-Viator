from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

index_page = Blueprint('index', __name__,
                        template_folder='templates')

@index_page.route('/')
def index():
    try:
        return render_template('index.html')
    except TemplateNotFound:
        abort(404)
