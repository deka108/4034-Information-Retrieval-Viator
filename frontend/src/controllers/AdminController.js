function AdminController($scope, $q, $window, $mdDialog, DbDataService, SolrDataService, InitializationService, EVENTS) {
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
        $scope.pageIndexes = SolrDataService.getPageIndexes();
        console.log($scope.pageIds);
        console.log($scope.pageIndexes);
    });

    $scope.$on(EVENTS.PAGE_ID_RECEIVED, function() {
        $scope.pageIds = DbDataService.getPageIds();
    });

    $scope.$on(EVENTS.PAGE_INDEX_RECEIVED, function() {
        $scope.pageIndexes = SolrDataService.getPageIndexes();
    });

    $scope.$on(EVENTS.PAGE_MODIFIED, function() {
        $scope.dbPromise = DbDataService.retrievePageIds();
    });

    $scope.$on(EVENTS.PAGE_INDEX_MODIFIED, function() {
        $scope.solrPromise = SolrDataService.retrievePageIndexes();
    });

    // initialization
    if ($scope.isInitial) {
        $scope.loadingPromise = InitializationService.initialize();
        let circularProgressTop = 35;
        let loadingMessageTop = 50;
        let h = $window.innerHeight;

        $scope.circularTopPos = {
            top: Math.round(h * circularProgressTop / 100.0) + 'px'
        };

        $scope.loadingMessageTopPos = {
            top: Math.round(h * loadingMessageTop / 100.0) + 'px'
        };
    }

    // dummy token (need to implement!!!!)
    $scope.token = "dummy_token";

    $scope.showGetTokenDialog = function(ev, pageId) {
        $scope.pageId = pageId;
        $mdDialog.show({
            contentElement: '#tokenDialog',
            parent: angular.element(document.body),
            targetEvent: ev,
            clickOutsideToClose: true
        });
    };

    $scope.crawlPage = function(pageId) {
        // get token first
        DbDataService.crawlFacebookPage($scope.token, pageId);
    }

    $scope.crawlAllPages = function() {
        // get token first
        DbDataService.crawlAllPages($scope.token);
    }

    $scope.deleteData = function(pageId) {
        DbDataService.deleteFacebookPageData(pageId);
    }

    $scope.deleteData = function(pageId) {
        DbDataService.deleteFacebookPageData(pageId);
    }

    $scope.reindexAllPages = function() {
        SolrDataService.reindexAllPageData();
    }

    $scope.reindexPage = function(pageId) {
        SolrDataService.reindexFacebookPageData(pageId);
    }

    $scope.deleteAllIndexes = function() {
        SolrDataService.deleteAllIndex();
    }

    $scope.deleteIndex = function(pageId) {
        SolrDataService.deleteFacebookPageIndex(pageId);
    }

    $scope.getAllIndex = function() {

    };

    $scope.selected = [];

    $scope.query = {
        order: 'name',
        limit: 10,
        page: 1
    };

    function DialogController($scope, $mdDialog) {
        $scope.hide = function() {
            $mdDialog.hide();
        };

        $scope.cancel = function() {
            $mdDialog.cancel();
        };

        $scope.answer = function(answer) {
            $mdDialog.hide(answer);
        };
    }

}

export default ['$scope', '$q', '$window', '$mdDialog', 'DbDataService', 'SolrDataService', 'InitializationService', 'EVENTS', AdminController];