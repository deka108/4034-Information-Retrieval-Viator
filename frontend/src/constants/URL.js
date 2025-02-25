const BASE_URL = 'http://localhost:8888';
const DB_MANAGER_URL = BASE_URL + '/db';
const SOLR_MANAGER_URL = BASE_URL + '/solr';

const URL = {
    SEARCH_URL: BASE_URL + '/search/',
    SEARCH_MORE_URL: BASE_URL + '/search/more/',

    DB_CRAWL: DB_MANAGER_URL + '/crawl/',
    DB_READ_PAGES: DB_MANAGER_URL + '/db_records/',
    DB_READ_POSTS: DB_MANAGER_URL + '/read',
    DB_DELETE: DB_MANAGER_URL + '/delete/',
    SOLR_READ: DB_MANAGER_URL + '/solr_records/',

    SOLR_INDEXING: SOLR_MANAGER_URL + '/indexing/',
    SOLR_DELETE: SOLR_MANAGER_URL + '/delete/',

    CRAWL: DB_MANAGER_URL + '/crawl/'
}

export default URL;