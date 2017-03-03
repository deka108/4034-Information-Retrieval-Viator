function SolrDataService($http, $rootScope, URL, EVENTS) {
    function _on_page_index_received() {
        $rootScope.$broadcast(EVENTS.PAGE_INDEX_RECEIVED);
    }

    function _on_all_page_reindexed() {
        $rootScope.$broadcast(EVENTS.REINDEX_ALL_PAGES);
    }

    function _on_page_reindexed() {
        $rootScope.$broadcast(EVENTS.REINDEX_PAGE);
    }

    function _on_all_index_deleted() {
        $rootScope.$broadcast(EVENTS.DELETE_ALL_INDEX);
    }

    function _on_index_deleted() {
        $rootScope.$broadcast(EVENTS.DELETE_PAGE_INDEX);
    }

    function _update_page_indexes(newData) {
        pageIndexes = newData;
    }

    function _on_error(response) {
        if (response.status > 0) {
            console.error(response);
        }
    }

    let pageIndexes = null;

    // solr related
    this.getPageIndexes = function() {
        return pageIndexes;
    }

    this.retrievePageIndexes = function() {
        return $http.get(URL.SOLR_READ).then(
            function success(response) {
                _on_page_index_received();
                _update_page_indexes(response.data);
            },
            function error(response) {
                _on_error(response);
            });
    }

    this.reindexAllPageData = function() {
        return $http.get(URL.SOLR_INDEXING).then(
            function success(response) {
                _on_all_page_reindexed();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.reindexFacebookPageData = function(page_id) {
        return $http.get(URL.SOLR_INDEXING + page_id).then(
            function success(response) {
                _on_page_reindexed();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.deleteAllIndex = function() {
        return $http.get(URL.SOLR_DELETE).then(
            function success(response) {
                _on_all_index_deleted();
            },
            function error(response) {
                _on_error(response);
            }
        );
    };

    this.deleteFacebookPageIndex = function(page_id) {
        return $http.get(URL.SOLR_DELETE + page_id).then(
            function success(response) {
                _on_index_deleted();
            },
            function error(response) {
                _on_error(response);
            }
        );
    };

}

export default ['$http', '$rootScope', 'URL', 'EVENTS', SolrDataService]