function SearchController($scope, PostDataService, EVENTS, _) {
    $scope.curOrder = null;

    $scope.searchFilters = [{
            category: 'Emotions',
            values: ['Happy', 'Sad', 'Angry']
        },
        {
            category: 'Country',
            values: ['Indonesia', 'Japan', 'Malaysia', 'Singapore']
        }
    ];

    $scope.searchOrders = [
        { value: null },
        { value: 'Likes' },
        { value: 'Message' },
        { value: 'Country' }
    ];

    $scope.update = function() {
        console.log($scope.selectedFilterCategory);
    };

    $scope.sortBy = function(order) {
        $scope.currOrder = order.value ? order.value.toLowerCase() : null;
    };

    $scope.searchQuery = function(query) {
        PostDataService.retrieveQueryResult(query);
    }

    $scope.getPostByPageId = function(pageId) {
        PostDataService.retrievePostDataByPageId(pageId);
    };

    $scope.$on(EVENTS.POST_DATA_RECEIVED, function() {
        let postDataTemp = PostDataService.getPostData();

        if (postDataTemp instanceof Array) {
            $scope.postData = _.flatMap(postDataTemp, data => data.data);
        }
    });

    $scope.$on(EVENTS.SEARCH_RESULTS_RECEIVED, function() {
        let postDataTemp = PostDataService.getSearchResult();

        if ("response" in postDataTemp) {
            // $scope.searchResult = _.flatMap(postDataTemp.response, data => data.docs);
            // console.log($scope.searchResult);
            // $scope.postSearchResult = postDataTemp.response.docs;
            $scope.postSearchResult = postDataTemp.highlighting;
        }

    });

}

export default ['$scope', 'PostDataService', 'EVENTS', '_', SearchController];