function SearchController($scope, SolrDataService, EVENTS, _) {

    $scope.curOrder = null;
    $scope.curPage = 0;
    $scope.existNextPage = false;
    $scope.suggestions = [];
    $scope.filter = {};
    $scope.filter.TimeStart = new Date();
    $scope.filter.TimeEnd = new Date();
    $scope.filter.PageID = null;
    $scope.filter.Topic = null;
    $scope.filter.Sentiment = null;
    $scope.curSort = 'Relevance';
    $scope.order = 'Ascending';

    $scope.searchSorts = [
        'Relevance',
        'Time',
        'Reactions',
        'Shares',
    ];

    $scope.orderOptions = ['Ascending', 'Descending'];

    // $scope.refreshSortState = function() {
    //     $scope.boolSort = {
    //         'Time': $scope.curSort == 'Time',
    //         'Reactions': $scope.curSort == 'Reactions',
    //         'Shares': $scope.curSort == 'Shares',
    //     }
    // }

    $scope.searchFilters = [
        null,
        'Time',
        'PageID',
        'Topic',
        'Sentiment',
        'Nearby',
    ];

    $scope.sentimentOptions = ['Positive', 'Neutral', 'Negative'];
    $scope.topicOptions = ['Food', 'Event', 'Nature', 'Attraction', 'Accomodation'];

    $scope.refreshFilterDate = function() {
        $scope.filter.Time = '[' + $scope.filter.TimeStart + ' TO ' + $scope.filter.TimeEnd + ']';
        // console.log($scope.filter.Time);
    }

    $scope.searchQuery = function() {
        $scope.curPage = 0;
        SolrDataService.retrieveQueryResult($scope.searchData.textQuery, 0, $scope.curSort, $scope.order);
    }

    $scope.searchQueryNextPage = function() {
        if($scope.existNextPage) {
            $scope.curPage++;
            SolrDataService.retrieveQueryResult($scope.searchData.textQuery, $scope.curPage, $scope.curSort, $scope.order);
        }
    }
    $scope.searchQueryPrevPage = function() {
        if($scope.curPage > 0) {
            $scope.curPage--;
            SolrDataService.retrieveQueryResult($scope.searchData.textQuery, $scope.curPage, $scope.curSort, $scope.order);
        }
    }

    $scope.getMoreLikeThis = function(key, pageId){
        SolrDataService.retrieveMoreLikeThis(key, pageId);
    }

    $scope.$on(EVENTS.SEARCH_RESULT_RECEIVED, function() {
        let searchResultTemp = SolrDataService.getSearchResults();

        if ("response" in searchResultTemp) {
            $scope.searchResult = {
                docs: searchResultTemp.response.docs,
                docsCount: searchResultTemp.response.numFound,
                queryTime: searchResultTemp.responseHeader.QTime,
                highlighting: searchResultTemp.response.highlighting,
                suggestions: searchResultTemp.spellcheck.suggestions,
            }

            $scope.existNextPage = searchResultTemp.next_page;
            updateHighlight($scope.searchResult.docs, searchResultTemp.highlighting);
            if($scope.searchResult.suggestions != false){
                $scope.suggestions = reparse($scope.searchResult.suggestions);
            } else $scope.suggestions = false;

            // console.log($scope.suggestions);
            _reset_form();
        }

    });

    $scope.$on(EVENTS.MORE_LIKE_THIS_RECEIVED, function(){
        let tempMoreLikeThis = SolrDataService.getMoreLikeThisData();
        let postId = $scope.searchResult.docs[tempMoreLikeThis.key].id;
        let moreLikeThisResults = tempMoreLikeThis.data.moreLikeThis[postId].docs;
        moreLikeThisResults.forEach(function(value, index) {
            value.span  = { row : 1, col : 1 };
            switch(index+1) {
                case 1:
                    value.span.row = value.span.col = 2;
                    break;
                case 4:
                    value.span.row = value.span.col = 2;
                    break;
                case 5:
                    value.span.col = 2;
                    break;
            }
            value.bgImage = 'background-image: ' + value.full_picture;
            value.fontSize = { 'font-size': (value.span.col*4+8) + 'px' };
        })
        console.log(moreLikeThisResults);
        $scope.searchResult.docs[tempMoreLikeThis.key].moreLikeThis = moreLikeThisResults;


    })

    function reparse(suggestions){
        let result=[];
        suggestions.forEach(function(val, i){
            if(i%2 == 0){
                let value = {'mispelled': suggestions[i],
                'replacements': suggestions[i+1].suggestion,
                'startOffset': suggestions[i+1].startOffset,
                'endOffset': suggestions[i+1].endOffset
                };
                result.push(value);
            }
        })
        return result;
    }

    // function combinations(suggestions) {
    //     let sgList = [];
    //     let suggested = $scope.searchData.textQuery;
    //     suggestions.forEach(function (val, i){
    //         if(i%2 == 0){
    //             suggestions[i+1].suggestion.forEach(function (subst){
    //                 sgList.unshift(replaceRange(suggested, suggestions[i+1].startOffset, suggestions[i+1].endOffset, subst));
    //             })
    //         }
    //     })
    //     for(let j=0; j<suggestions.length/2; j++){
    //         sgList.forEach(function (text, i){
    //             suggestions.forEach(function (val, i){
    //                 if(i%2 == 0){
    //                     suggestions[i+1].suggestion.forEach(function (subst){
    //                         sgList.unshift(replaceRange(text, suggestions[i+1].startOffset, suggestions[i+1].endOffset, subst));
    //                     })
    //                 }
    //             })
    //         })
    //     }
    //     return sgList.filter( function( item, index, inputArray ) {
    //        return inputArray.indexOf(item) == index;
    //     }).slice(0,2);
    // }

    $scope.replaceQuery = function(start, end, substitute){
        $scope.searchData.textQuery = replaceRange($scope.searchData.textQuery, start, end, substitute);
        console.log($scope.searchData.textQuery);
        $scope.searchQuery();
    }

    function replaceRange(s, start, end, substitute) {
        return s.substring(0, start) + substitute + s.substring(end);
    }

    function updateHighlight(docs, highlighting) {
        docs.forEach(function (i) {

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
        // $scope.searchData = {};
        $scope.searchForm.$setPristine();
        $scope.searchForm.$setUntouched();
    }

}

export default ['$scope', 'SolrDataService', 'EVENTS', '_', SearchController];