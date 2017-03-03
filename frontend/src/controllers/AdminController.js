function AdminController($scope, DbDataService, SolrDataService) {
    $scope.delay = 0;
    $scope.minDuration = 0;
    $scope.message = 'Loading...';
    $scope.backdrop = true;

    $scope.setPromise = function(promise) {
        $scope.myPromise = promise;
    };

    // initialization
    if ($scope.isInitial) {
        // $scope.myPromise = GraphDataFactory.getExampleGraphData();
        let circularProgressTop = 35;
        let loadingMessageTop = 50;
        let h = $window.innerHeight;

        $scope.circularTopPos = {
            top: Math.round(h * circularProgressTop / 100.0) + 'px'
        };

        $scope.loadingMessageTopPos = {
            top: Math.round(h * loadingMessageTop / 100.0) + 'px'
        };
    }

    $scope.getAllIndex();

    $scope.selected = [];

    $scope.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

}

export default ['$scope', 'DbDataService', 'SolrDataService', AdminController];