import os


DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SOLR_BASE_URL = 'http://localhost:4000/solr/'
SOLR_UPDATE_JSON_URL = SOLR_BASE_URL + "viator_core/update/json/docs"

DATA_DIR = os.path.join(BASE_DIR, 'data')
JSON_DATA_PATH = os.path.join(DATA_DIR, '%s')

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"


def get_data_path(file_name):
    return os.path.join(DATA_DIR, file_name)