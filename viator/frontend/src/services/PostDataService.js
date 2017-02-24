function PostDataService($http, $rootScope, EVENTS, URL){
    function _updateData(data){
        $rootScope.$broadcast(EVENTS.RECEIVE_DATA, data);
    }

    this.getData = function(country){
        $http.get(URL.DATA_URL + country).then(
        function success(response){
            console.log(response);
        }, 
        function error(response){
            console.error(response);
        });
    }

    this.createData = function(){
        $http.get(URL.DB_CREATE).then(
        function success(response){
            console.log(response);
            _updateData(response.data);
        }, 
        function error(response){
            if (response.status > 0){
                console.error(response);
            }
        });
    }
}

export default ['$http', '$rootScope', 'EVENTS', 'URL', PostDataService]