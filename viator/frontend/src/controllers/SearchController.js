function SearchController($scope) {
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
        { value: 'Likes' },
        { value: 'Country' }
    ];

    $scope.update = function() {
        console.log($scope.selectedFilterCategory);
    }
}

export default ['$scope', SearchController];