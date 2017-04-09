function InitializationService($q, $rootScope, DbDataService, SolrDataService, URL, EVENTS) {
    function _on_initialized() {
        $rootScope.$broadcast(EVENTS.INITIALIZATION_FINISHED);
        console.log("Initialized");
    }

    function _on_error(err) {
        console.error(err);
    }

    this.initialize = function() {
        $q.all([
            DbDataService.retrievePostIds(0),
            DbDataService.retrievePageIds(),
            SolrDataService.retrievePageIndexes()
        ]).then((values) => { _on_initialized() }, (err) => _on_error(err));
    }

}

export default ['$q', '$rootScope', 'DbDataService', 'SolrDataService', 'URL', 'EVENTS', InitializationService];