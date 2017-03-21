function AdminController($scope, $q, $window, $mdDialog, DbDataService, SolrDataService, InitializationService, EVENTS, _) {
    $scope.isInitial = true;
    $scope.delay = 0;
    $scope.minDuration = 0;
    $scope.message = 'Loading...';
    $scope.backdrop = true;

    $scope.setPromise = function(promise) {
        $scope.loadingPromise = promise;
    };

    $scope.$on(EVENTS.INITIALIZATION_FINISHED, function() {
        $scope.isInitial = false;
        $scope.pageIds = DbDataService.getPageIds();
        $scope.updatePageIndexes(SolrDataService.getPageIndexes());
        // $scope.displayPageIndexes();
        console.log($scope.pageIds);
        console.log($scope.pageIndexes);
    });

    $scope.$on(EVENTS.PAGE_ID_RECEIVED, function() {
        $scope.pageIds = DbDataService.getPageIds();
        $scope.pageIdsCount = _.size($scope.pageIds);
    });

    $scope.$on(EVENTS.PAGE_INDEX_RECEIVED, function() {
        $scope.updatePageIndexes(SolrDataService.getPageIndexes());
    });

    $scope.updatePageIndexes = function(response) {
        $scope.tmpPageIndexes = response.facet_counts.facet_fields.page_id;
        $scope.pageIndexCounts = $scope.tmpPageIndexes.length/2;
        
        $scope.displayPageIndexes();

        // for (let i = 0; i < tmpPageIndexes.length; i++) {
        //     if (i % 2 == 0) {
        //         prev = tmpPageIndexes[i];
        //         // console.log(prev);
        //     } else {
        //         $scope.pageIndexes[prev] = tmpPageIndexes[i];
        //     }
        // }

        // $scope.pageIndexCounts = _.size($scope.pageIndexes);
    }

    $scope.displayPageIndexes = function(){
        $scope.pageIndexes = {};
        let prev = "";

        for (let i = ($scope.query.page-1)*$scope.query.limit*2; i < ($scope.query.page * $scope.query.limit)*2 && i < $scope.tmpPageIndexes.length; i++) {
            if (i % 2 == 0) {
                prev = $scope.tmpPageIndexes[i];
                // console.log(prev);
            } else {
                $scope.pageIndexes[prev] = $scope.tmpPageIndexes[i];
            }
        }
    }

    $scope.$on(EVENTS.PAGE_MODIFIED, function() {
        $scope.dbPromise = DbDataService.retrievePageIds();
    });

    // $scope.solrPromise = SolrDataService.retrievePageIndexes();

    $scope.$on(EVENTS.PAGE_INDEX_MODIFIED, function() {
        $scope.solrPromise = SolrDataService.retrievePageIndexes();
    });

    // initialization
    if ($scope.isInitial) {
        $scope.loadingPromise = InitializationService.initialize();
        // let circularProgressTop = 35;
        // let loadingMessageTop = 50;
        // let h = $window.innerHeight;

        // $scope.circularTopPos = {
        //     top: Math.round(h * circularProgressTop / 100.0) + 'px'
        // };

        // $scope.loadingMessageTopPos = {
        //     top: Math.round(h * loadingMessageTop / 100.0) + 'px'
        // };
    }

    $scope.showGetTokenDialog = function(ev, pageId) {
        $mdDialog.show({
            controller: DialogController,
            templateUrl: 'token_dialog.html',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true,
            fullscreen: true
        }).then(function(token) {
            if (token) {
                if (pageId) {
                    DbDataService.crawlFacebookPage(token, pageId);
                } else {
                    DbDataService.crawlAllPages(token);
                }
            }
        }, () => console.log("Cancelled"));
    };

    $scope.deleteData = function(pageId) {
        DbDataService.deleteFacebookPageData(pageId);
    }

    $scope.deleteData = function(pageId) {
        DbDataService.deleteFacebookPageData(pageId);
    }

    $scope.reindexAllPages = function() {
        $scope.setPromise(SolrDataService.reindexAllPageData());
    }

    $scope.reindexPage = function(pageId) {
        $scope.setPromise(SolrDataService.reindexFacebookPageData(pageId));
    }

    $scope.deleteAllIndexes = function() {
        $scope.setPromise(SolrDataService.deleteAllIndex());
    }

    $scope.deleteIndex = function(pageId) {
        $scope.setPromise(SolrDataService.deleteFacebookPageIndex(pageId));
    }

    $scope.getAllIndex = function() {

    };

    $scope.selected = [];

    $scope.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

    function DialogController($scope, $mdDialog, $window, DbDataService) {
        $scope.hide = function() {
            $mdDialog.hide();
        };

        $scope.cancel = function() {
            $mdDialog.cancel();
        };

        $scope.getTokenFromFacebook = function() {
            // $window.open('https://facebook.com', '_blank');
            // change to facebook  page for generating token
            $window.open('https://developers.facebook.com/tools/explorer/', '_blank');
        }

        $scope.crawl = function(token) {
            $mdDialog.hide(token);
        };
    }
}

export default ['$scope', '$q', '$window', '$mdDialog', 'DbDataService', 'SolrDataService', 'InitializationService', 'EVENTS', '_', AdminController];