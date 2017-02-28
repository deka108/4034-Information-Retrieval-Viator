function SearchController($scope, PostDataService) {

    $scope.currOrder = null;

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

    $scope.callService = function(textQuery){
        PostDataService.getData(textQuery).then(function success (response) {
            $scope.data = response.data;
        }, function failure (response) {
            console.log(response);
        })
    };

    $scope.sortBy = function(order) {
        $scope.currOrder = order.value? order.value.toLowerCase() : null;
    }

    // $scope.$on(EVENTS.RECEIVE_DATA, function(event, fetchedData){
    //     $scope.data = fetchedData;
    //     console.log(fetchedData.data.data);
    // });

}

export default ['$scope', 'PostDataService', SearchController];