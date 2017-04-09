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
    $scope.filter.Popularity = 'Normal';
    $scope.filter.Nearby = 0;
    $scope.curFilter = 'None';
    $scope.curSort = 'Relevance';
    $scope.order = 'Descending';
    $scope.curGeolocation = '0,0';

    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                $scope.curGeolocation = position.coords.latitude + ',' + position.coords.longitude;
                console.log("success get geolocation");
                console.log($scope.curGeolocation);
            },
            (position) => {
                $scope.curGeolocation = '0,0';
                console.log('failed to get geolocation');
            }
        );
    } else {
        console.error('does not support geolocation');
        $scope.curGeolocation = '0,0';
    }

    $scope.searchSorts = [
        'Relevance',
        'Time',
        'Reactions',
        'Popularity',
    ];

    $scope.orderOptions = ['Ascending', 'Descending'];


    $scope.refreshOrder = function(order) {
        $scope.order = order;
    }

    $scope.searchFilters = [
        'None',
        'Time',
        'PageID',
        'Topic',
        'Sentiment',
        'Nearby',
        'Popularity',
    ];

    $scope.sentimentOptions = ['Very Positive', 'Positive', 'Neutral', 'Negative'];

    $scope.popOptions = ['Normal', 'Popular', 'Very Popular', 'Extremely Popular'];

    $scope.sentimentIcon = {
        'very_positive': 'mood',
        'positive': 'sentiment_satisfied',
        'neutral': 'sentiment_neutral',
        'negative': 'sentiment_very_dissatisfied',
    }
    $scope.topicOptions = ['Food', 'Event', 'Nature', 'Attraction', 'Accomodation'];

    $scope.refreshFilterDate = function() {
        $scope.filter.Time = '[' + $scope.filter.TimeStart.toISOString() + ' TO ' + $scope.filter.TimeEnd.toISOString() + ']';
        console.log($scope.filter.Time);
    }

    $scope.searchQuery = function() {
        $scope.curPage = 0;
        let filter = $scope.curFilter;
        let filter_query = $scope.filter[filter];
        if (filter == 'Topic' || filter == 'Sentiment' || filter == 'Popularity') {
            filter_query = filter_query.toLowerCase();
        }
        if (filter == 'None') {
            filter = null;
        }
        console.log(filter_query);
        SolrDataService.retrieveQueryResult($scope.searchData.textQuery, 0, $scope.curSort, $scope.order, filter, filter_query, $scope.curGeolocation);
    }

    $scope.searchQueryNextPage = function() {
        if ($scope.existNextPage) {
            $scope.curPage++;
            SolrDataService.retrieveQueryResult($scope.searchData.textQuery, $scope.curPage, $scope.curSort, $scope.order);
        }
    }
    $scope.searchQueryPrevPage = function() {
        if ($scope.curPage > 0) {
            $scope.curPage--;
            SolrDataService.retrieveQueryResult($scope.searchData.textQuery, $scope.curPage, $scope.curSort, $scope.order);
        }
    }

    $scope.getMoreLikeThis = function(key, pageId) {
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
            $scope.searchResult.docs.forEach((value, index) => {
                value.date = new Date(value.time);
            });
            updateHighlight($scope.searchResult.docs, searchResultTemp.highlighting);
            if ($scope.searchResult.suggestions != false) {
                $scope.suggestions = reparse($scope.searchResult.suggestions);
            } else $scope.suggestions = false;

            // console.log($scope.suggestions);
            _reset_form();
        }

    });

    $scope.$on(EVENTS.MORE_LIKE_THIS_RECEIVED, function() {
        let tempMoreLikeThis = SolrDataService.getMoreLikeThisData();
        let postId = $scope.searchResult.docs[tempMoreLikeThis.key].id;
        let moreLikeThisResults = tempMoreLikeThis.data.moreLikeThis[postId].docs;
        moreLikeThisResults.forEach(function(value, index) {
            value.span = { row: 1, col: 1 };
            switch (index + 1) {
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
            value.fontSize = { 'font-size': (value.span.col * 4 + 8) + 'px' };
        })
        console.log(moreLikeThisResults);
        $scope.searchResult.docs[tempMoreLikeThis.key].moreLikeThis = moreLikeThisResults;


    })

    function reparse(suggestions) {
        let result = [];
        suggestions.forEach(function(val, i) {
            if (i % 2 == 0) {
                let value = {
                    'mispelled': suggestions[i],
                    'replacements': suggestions[i + 1].suggestion,
                    'startOffset': suggestions[i + 1].startOffset,
                    'endOffset': suggestions[i + 1].endOffset
                };
                result.push(value);
            }
        })
        return result;
    }

    $scope.replaceQuery = function(start, end, substitute) {
        $scope.searchData.textQuery = replaceRange($scope.searchData.textQuery, start, end, substitute);
        console.log($scope.searchData.textQuery);
        $scope.searchQuery();
    }

    function replaceRange(s, start, end, substitute) {
        return s.substring(0, start) + substitute + s.substring(end);
    }

    function updateHighlight(docs, highlighting) {
        docs.forEach(function(i) {

            if (highlighting[i.id]) {
                if (highlighting[i.id].message) {
                    i.message = highlighting[i.id].message;
                }
                if (highlighting[i.id].name) {
                    i.name = highlighting[i.id].name;
                }
                if (highlighting[i.id].desc) {
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