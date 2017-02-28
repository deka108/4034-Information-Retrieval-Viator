function SolrDataService($http, $rootScope, URL, EVENTS) {
    function _on_receive_pageids() {
        $rootScope.$broadcast(EVENTS.PAGE_ID_RECEIVED);
    }

    function _update_post_data(newData) {
        postData = newData;
    }

    function _update_pageids(newData) {
        pageIds = newData;
    }

    function _on_error(response) {
        if (response.status > 0) {
            console.error(response);
        }
    }

    let pageIds = null;

    this.getPostData = function() {
        return postData;
    }

    this.retrievePageIds = function() {
        return $http.get(URL.DB_READ).then(
            function success(response) {
                _update_pageids(response.data);
                _on_receive_pageids();
            },
            function error(response) {
                _on_error(response);
            }
        )
    }

    this.reindexAllDataInServer = function() {

    }

    this.deleteAllIndex = function() {

    }

    this.reindexNewFacebookPage = function() {

    }

    this.reindexExistingFacebookPageIndex = function(facebookPage) {

    }

    this.deleteExistingFacebookPageIndex = function(facebookPage) {

    }
}

export default ['$http', '$rootScope', 'URL', 'EVENTS', SolrDataService]