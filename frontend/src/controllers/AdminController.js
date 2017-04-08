function AdminController($scope, $q, $window, $mdDialog, $interval, DbDataService, SolrDataService, InitializationService, EVENTS, _) {
    $scope.isInitial = true;
    $scope.delay = 0;
    $scope.minDuration = 0;
    $scope.message = 'Loading...';
    $scope.backdrop = true;

    $scope.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

    $scope.dataQuery = {
        order: 'name',
        limit: 10,
        page: 1
    };

    $scope.postQuery = {
        order: 'name',
        limit: 10,
        page: 1
    };

    $scope.setPromise = function(promise) {
        $scope.loadingPromise = promise;
    };

    $scope.$on(EVENTS.INITIALIZATION_FINISHED, function() {
        $scope.isInitial = false;
        $scope.postIds = DbDataService.getPostIds();
        $scope.pageIds = DbDataService.getPageIds();
        $scope.updatePageIndexes(SolrDataService.getPageIndexes());
        console.log($scope.postIds);
        console.log($scope.pageIds);
        console.log($scope.pageIndexes);
    });

    $scope.$on(EVENTS.PAGE_ID_RECEIVED, function() {
        $scope.pageIds = DbDataService.getPageIds();
        $scope.pageIdsCount = _.size($scope.pageIds);
    });

    $scope.$on(EVENTS.POST_ID_RECEIVED, function() {
        let total = 0;
        for( let value in $scope.pageIds){
            total += $scope.pageIds[value].count;
        }
        $scope.postIds = DbDataService.getPostIds();
        $scope.postIdsCount = total;
    });

    $scope.$on(EVENTS.PAGE_INDEX_RECEIVED, function() {
        $scope.updatePageIndexes(SolrDataService.getPageIndexes());
    });

    $scope.updatePageIndexes = function(response) {
        console.log(response);
        $scope.pageIndexes = response;
    }

    $scope.$on(EVENTS.PAGE_MODIFIED, function() {
        $scope.dbPromise = DbDataService.retrievePageIds();
        $scope.dbPromise = DbDataService.retrievePostIds($scope.postQuery.page - 1);
    });

    $scope.$on(EVENTS.PAGE_INDEX_MODIFIED, function() {
        $scope.solrPromise = SolrDataService.retrievePageIndexes();
    });

    // initialization
    if ($scope.isInitial) {
        $scope.loadingPromise = InitializationService.initialize();
    }

    $scope.displayPostIds = function() {
        DbDataService.retrievePostIds($scope.postQuery.page);
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

    function DialogController($scope, $mdDialog, $window, DbDataService) {
        $scope.hide = function() {
            $mdDialog.hide();
        };

        $scope.cancel = function() {
            $mdDialog.cancel();
        };

        $scope.getTokenFromFacebook = function() {
            // change to facebook  page for generating token
            $window.open('https://developers.facebook.com/tools/explorer/', '_blank');
        }

        $scope.crawl = function(token) {
            $mdDialog.hide(token);
        };
    }

}

export default ['$scope', '$q', '$window', '$mdDialog', '$interval', 'DbDataService', 'SolrDataService', 'InitializationService', 'EVENTS', '_', AdminController];