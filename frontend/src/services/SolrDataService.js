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

    function _on_more_like_this_received() {
        $rootScope.$broadcast(EVENTS.MORE_LIKE_THIS_RECEIVED);
    }

    function _update_page_indexes(newData) {
        pageIndexes = newData;
    }

    function _update_search_results(newData) {
        searchResults = newData;
    }

    function _update_more_like_this(data, key){
        moreLikeThis = {'data': data, 'key': key}
    }

    function _on_error(response) {
        if (response.status > 0) {
            console.error(response);
        }
    }

    let pageIndexes = null;
    let searchResults = null;
    let moreLikeThis = null;

    // solr related
    this.getSearchResults = function() {
        return searchResults;
    }

    this.getPageIndexes = function() {
        return pageIndexes;
    }

    this.getMoreLikeThisData = function() {
        return moreLikeThis;
    }

    this.retrieveQueryResult = function(query, page, sort, order, filter, filter_query, geoLocation) {
        let data = {
            'q': query,
            'p': page,
            's': sort.toLowerCase(),
            'o': order.toLowerCase(),
            'f': filter? filter.toLowerCase() : null,
            'fq': filter_query,
            'gl': geoLocation,
        }
        return $http.post(URL.SEARCH_URL, data).then(
            function success(response) {
                _update_search_results(response.data);
                _on_search_result_received();
            },
            function error(response) {
                _on_error(response);
            }
        )
    }

    this.retrieveMoreLikeThis = function(key, postId) {
        return $http.post(URL.SEARCH_MORE_URL, { p: postId }).then(
            function success(response){
                _update_more_like_this(response.data, key);
                _on_more_like_this_received();
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