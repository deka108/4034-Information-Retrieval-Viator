const BASE_URL = 'http://localhost:8888';
const DB_MANAGER_URL = BASE_URL + '/db';
const SOLR_MANAGER_URL = BASE_URL + '/solr';

const URL = {
    SEARCH_URL: BASE_URL + '/search/',

    DB_CRAWL: DB_MANAGER_URL + '/crawl/',
    DB_READ: DB_MANAGER_URL + '/read/',
    DB_DELETE: DB_MANAGER_URL + '/delete/',

    SOLR_READ: SOLR_MANAGER_URL + '/read/',
    SOLR_INDEXING: SOLR_MANAGER_URL + '/indexing/',
    SOLR_DELETE: SOLR_MANAGER_URL + '/delete/',

    CRAWL: DB_MANAGER_URL + '/crawl/'
}

export default URL;