function SearchController($scope, SolrDataService, EVENTS, _) {
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

    $scope.searchQuery = function() {
        // console.log($scope.searchData.textQuery);
        SolrDataService.retrieveQueryResult($scope.searchData.textQuery);
    }

    $scope.$on(EVENTS.SEARCH_RESULT_RECEIVED, function() {
        let searchResultTemp = SolrDataService.getSearchResults();

        if ("response" in searchResultTemp) {
            $scope.searchResult = {
                docs: searchResultTemp.response.docs,
                docsCount: searchResultTemp.response.numFound,
                queryTime: searchResultTemp.responseHeader.QTime,
                highlighting: searchResultTemp.response.highlighting
            }

            updateHighlight($scope.searchResult.docs, searchResultTemp.highlighting);

            console.log($scope.searchResult);
            _reset_form();
        }

    });

    function updateHighlight(docs, highlighting) {
        docs.forEach(function (i) {
            // console.log(i);
            console.log(highlighting[i.id]);
            if(highlighting[i.id]){
                if(highlighting[i.id].message){
                    i.message = highlighting[i.id].message;
                }
                if(highlighting[i.id].name){
                    i.name = highlighting[i.id].name;
                }
                if(highlighting[i.id].desc){
                    i.desc = highlighting[i.id].desc;
                }
            }
        })
    }

    function _reset_form() {
        $scope.searchData = {};
        $scope.searchForm.$setPristine();
        $scope.searchForm.$setUntouched();
    }

}

export default ['$scope', 'SolrDataService', 'EVENTS', '_', SearchController];