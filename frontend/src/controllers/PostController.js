function PostController($scope, DbDataService, EVENTS, _) {
    $scope.$on(EVENTS.POST_DATA_RECEIVED, function() {
        let postDataTemp = DbDataService.getPostData();

        if (postDataTemp instanceof Array) {
            $scope.postData = _.flatMap(postDataTemp, data => data.data);
        }
    });

    $scope.getPostsByPostId = function() {
        DbDataService.retrievePostByPageId($scope.)
    }

}

export default ['$scope', 'DbDataService', 'EVENTS', '_', SearchController];