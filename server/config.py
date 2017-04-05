import os


DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SOLR_ADMIN_URL = 'http://localhost:8983/solr/admin'
SOLR_BASE_URL = 'http://localhost:8983/solr/viator_core'

DATA_DIR = os.path.join(BASE_DIR, 'data')
JSON_DATA_PATH = os.path.join(DATA_DIR, '%s')
RECORDS_DATA_PATH = os.path.join(DATA_DIR, 'records.json')
RECORDS_TIME_DATA_PATH = os.path.join(DATA_DIR, 'records_time.json')
SPLITTED_DATA_PATH = os.path.join(DATA_DIR, 'splitted_data_for_labelling')
LABELLED_DATA_PATH = os.path.join(DATA_DIR,'labelled_data')
SCHEMA_DATA_PATH = os.path.join(DATA_DIR, 'schema.json')
INITIAL_RECORDS_DATA_PATH = os.path.join(DATA_DIR, 'initial_records.json')
STANFORD_POS_FILENAME = "stanford-postagger-full-2016-10-31"
STANFORD_POS_PATH = os.path.join(BASE_DIR,
                                 'core/nlp/{}'.format(STANFORD_POS_FILENAME))
STANFORD_NER_FILENAME = "stanford-ner-2016-10-31"
STANFORD_NER_PATH = os.path.join(BASE_DIR,
                                 'core/nlp/{}'.format(STANFORD_NER_FILENAME))

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"


def get_data_path(file_name):
    return os.path.join(DATA_DIR, file_name)


def get_splitted_data_path(file_name):
    if not os.path.exists(SPLITTED_DATA_PATH):
        os.makedirs(SPLITTED_DATA_PATH)
    return os.path.join(SPLITTED_DATA_PATH, file_name)

def get_labelled_data_path(file_name):
    if not os.path.exists(LABELLED_DATA_PATH):
        os.makedirs(LABELLED_DATA_PATH)
    return os.path.join(LABELLED_DATA_PATH,file_name)

def check_data_path(file_path):
    print(file_path)
    return os.path.isfile(file_path)


def get_stanford_pos(file):
    return os.path.join(STANFORD_POS_PATH, file)


def get_stanford_ner(file):
    return os.path.join(STANFORD_NER_PATH, file)