function DbDataService($http, $rootScope, URL, EVENTS) {
    function _on_page_id_received() {
        $rootScope.$broadcast(EVENTS.PAGE_ID_RECEIVED);
    }

    function _on_post_data_received() {
        $rootScope.$broadcast(EVENTS.POST_DATA_RECEIVED);
    }

    function _on_all_pages_crawled() {
        $rootScope.$broadcast(EVENTS.CRAWL_ALL_PAGES);
    }

    function _on_page_crawled() {
        $rootScope.$broadcast(EVENTS.CRAWL_PAGE);
    }

    function _on_all_pages_deleted() {
        $rootScope.$broadcast(EVENTS.DELETE_ALL_PAGES);
    }

    function _on_page_deleted() {
        $rootScope.$broadcast(EVENTS.DELETE_PAGE);
    }

    function _update_post_data(newData) {
        postData = newData;
    }

    function _update_page_ids(newData) {
        pageIds = newData;
    }

    function _update_page_infos(newData) {
        pageInfos = newData;
    }

    function _on_error(response) {
        if (response.status > 0) {
            console.error(response);
        }
    }

    let pageIds = null;
    let pageInfos = null;
    let postData = null;


    this.getPostData = function() {
        return postData;
    };

    this.getPageIds = function() {
        return pageIds;
    }

    this.getPageInfos = function() {
        return pageInfos;
    }

    // db related
    this.retrievePageIds = function() {
        return $http.get(URL.DB_READ).then(
            function success(response) {
                _update_page_ids(response.data);
                _on_page_id_received();
            },
            function error(response) {
                _on_error(response);
            }
        )
    }

    this.retrievePostByPageId = function(page_id) {
        return $http.get(URL.DB_READ + page_id).then(
            function success(response) {
                _update_post_data(response.data);
                _on_post_data_received();
            },
            function error(response) {
                _on_error(response);
            }
        );
    }

    this.crawlAllPages = function(data) {
        // send token
        return $http.post(URL.CRAWL, data).then(
            function success(response) {
                _on_all_pages_crawled();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.crawlFacebookPage = function(data) {
        // send token
        return $http.post(URL.CRAWL + page_id, data).then(
            function success(response) {
                _on_page_crawled();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.deleteAllData = function() {
        return $http.get(URL.DB_DELETE).then(
            function success(response) {
                _on_all_pages_deleted();
            },
            function error(response) {
                _on_error(response);
            });
    };

    this.deleteFacebookPageData = function(page_id) {
        return $http.get(URL.DB_DELETE).then(
            function success(response) {
                _on_page_deleted();
            },
            function error(response) {
                _on_error(response);
            });
    };

}

export default ['$http', '$rootScope', 'URL', 'EVENTS', DbDataService]