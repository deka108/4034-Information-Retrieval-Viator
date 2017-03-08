function SolrDataService($http, $rootScope, URL, EVENTS) {
    function _on_page_index_received() {
        $rootScope.$broadcast(EVENTS.PAGE_INDEX_RECEIVED);
    }

    function _on_search_result_received() {
        $rootScope.$broadcast(EVENTS.SEARCH_RESULT_RECEIVED);
    }

    function _on_page_index_modified() {
        $rootScope.$broadcast(EVENTS.PAGE_INDEX_MODIFIED);
    }

    function _update_page_indexes(newData) {
        pageIndexes = newData;
    }

    function _update_search_results(newData) {
        searchResults = newData;
    }

    function _on_error(response) {
        if (response.status > 0) {
            console.error(response);
        }
    }

    let pageIndexes = null;
    let searchResults = null;

    // solr related
    this.getSearchResults = function() {
        return searchResults;
    }

    this.getPageIndexes = function() {
        return pageIndexes;
    }

    this.retrieveQueryResult = function(query) {
        let data = {
            'q': query
        }

        return $http.post(URL.SEARCH_URL, data).then(
            function success(response) {
                console.log(response.data);
                _update_search_results(response.data);
                _on_search_result_received();
            },
            function error(response) {
                _on_error(response);
            }
        )
    }

    this.retrievePageIndexes = function() {
        return $http.get(URL.SOLR_READ).then(
            function success(response) {
                _update_page_indexes(response.data);
                _on_page_index_received();
            },
            function error(response) {
                _on_error(response);
            });
    }

    this.reindexAllPageData = function() {
        return $http.get(URL.SOLR_INDEXING).then(
            function success(response) {
                _on_page_index_modified();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.reindexFacebookPageData = function(page_id) {
        return $http.get(URL.SOLR_INDEXING + page_id).then(
            function success(response) {
                _on_page_index_modified();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.deleteAllIndex = function() {
        return $http.get(URL.SOLR_DELETE).then(
            function success(response) {
                _on_page_index_modified();
            },
            function error(response) {
                _on_error(response);
            }
        );
    };

    this.deleteFacebookPageIndex = function(page_id) {
        return $http.get(URL.SOLR_DELETE + page_id).then(
            function success(response) {
                _on_page_index_modified();
            },
            function error(response) {
                _on_error(response);
            }
        );
    };

}

export default ['$http', '$rootScope', 'URL', 'EVENTS', SolrDataService]