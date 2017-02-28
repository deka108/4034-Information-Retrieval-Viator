const BASE_URL = 'http://localhost:8888';
const DB_MANAGER_URL = BASE_URL + '/db';

const URL = {
    SEARCH_URL: BASE_URL + '/search/',
    DB_INDEXING: DB_MANAGER_URL + '/indexing/',
    DB_DELETE: DB_MANAGER_URL + '/delete/',
    DB_READ: DB_MANAGER_URL + '/read/'
}

export default URL;