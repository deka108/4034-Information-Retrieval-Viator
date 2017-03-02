import os


DEBUG = True

# Define the application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SOLR_ADMIN_URL = 'http://localhost:8983/solr/admin'
SOLR_BASE_URL = 'http://localhost:8983/solr/viator_core'

DATA_DIR = os.path.join(BASE_DIR, 'data')
JSON_DATA_PATH = os.path.join(DATA_DIR, '%s')
RECORDS_DATA_PATH = os.path.join(DATA_DIR, 'records.txt')
SCHEMA_DATA_PATH = os.path.join(DATA_DIR, 'schema.json')
INITIAL_PAGEID_PATH = os.path.join(DATA_DIR,'initial_pageid.txt')

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "secret"

# Secret key for signing cookies
SECRET_KEY = "secret"


def get_data_path(file_name):
    return os.path.join(DATA_DIR, file_name)