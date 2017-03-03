function AdminController($scope, PostDataService) {

    // $scope.getAllIndex = function(){
    //     PostDataService.getData('indonesia').then(function success (response) {
    //         $scope.index = response.data;
    //         $scope.indexLength =  $scope.index.length;
    //         // console.log(response.data);
    //     }, function failure (response) {
    //         console.log(response);
    //     })
    // };

    $scope.getAllIndex();

    $scope.selected = [];

    $scope.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

}

export default ['$scope', 'PostDataService', AdminController];