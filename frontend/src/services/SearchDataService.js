function SearchDataService($http, $rootScope, URL, EVENTS) {
    function _on_receive_data() {
        $rootScope.$broadcast(EVENTS.POST_DATA_RECEIVED);
    }

    function _on_receive_search_result() {
        $rootScope.$broadcast(EVENTS.SEARCH_RESULTS_RECEIVED);
    }

    function _update_post_data(newData) {
        postData = newData;
    }

    function _update_search_data(newData) {
        searchResult = newData;
    }

    function _on_error(response) {
        if (response.status > 0) {
            console.error(response);
        }
    }

    let postData = null;
    let searchResult = null;

    this.getPostData = function() {
        return postData;
    }

    this.getSearchResult = function() {
        return searchResult;
    }

    this.retrievePostDataByPageId = function(pageId) {
        return $http.get(URL.DB_READ + pageId).then(
            function success(response) {
                _update_post_data(response.data);
                _on_receive_data();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.retrieveQueryResult = function(query) {
        return $http.post(URL.SEARCH_URL, { query: query }).then(
            function success(response) {
                _update_search_data(response.data);
                console.log(response.data);
                _on_receive_search_result();
            },
            function error(response) {
                _on_error(response);
            });
    };
}

export default ['$http', '$rootScope', 'URL', 'EVENTS', SearchDataService]