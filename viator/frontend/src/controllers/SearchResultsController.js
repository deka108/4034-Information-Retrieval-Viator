function SearchResultsController($scope, EVENTS, PostDataService) {
    $scope.tests = [{
            'title': 'lucy',
            'description': 'hello ini lucy',
            'img-src': ''
        },
        {
            'title': 'deka',
            'description': 'hello ini deka',
            'img-src': ''
        },
        {
            'title': 'dita',
            'description': 'hello ini dita',
            'img-src': ''
        },
        {
            'title': 'felix',
            'description': 'hello ini felix',
            'img-src': ''
        },
        {
            'title': 'grace',
            'description': 'hello ini grace',
            'img-src': ''
        },
    ];

    $scope.callService = function(){
        PostDataService.getData('indonesia');
    }

    $scope.call2Service = function(){
        PostDataService.createData();
    }

    $scope.$on(EVENTS.RECEIVE_DATA, function(newData){
        $scope.data = newData;
    });
}

export default ['$scope', 'EVENTS', 'PostDataService', SearchResultsController]