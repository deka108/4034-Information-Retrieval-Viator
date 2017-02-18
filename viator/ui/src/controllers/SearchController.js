function SearchController($scope) {
    $scope.searchFilters = [{
            id: 1,
            category: 'Emotions',
            values: ['Happy', 'Sad', 'Angry']
        },
        {
            id: 2,
            category: 'Country',
            values: ['Indonesia', 'Japan', 'Malaysia', 'Singapore']
        }
    ];
    $scope.searchOrders = [
        { id: 1, value: 'Likes' },
        { id: 2, value: 'Country' }
    ];

    $scope.update = function() {
        console.log($scope.selectedFilterCategory);
    }
}

export default ['$scope', SearchController];