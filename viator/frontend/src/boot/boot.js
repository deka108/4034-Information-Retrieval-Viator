import angular from 'angular';

import App from 'src/app.js'
/**
 * Manually bootstrap the application when AngularJS and
 * the application classes have been loaded.
 */
angular
    .element(document)
    .ready(function() {
        angular
            .module('viator-bootstrap', [App.name])
            .run($rootScope => {
                console.log(`Running the 'viator-bootstrap'`);
                $rootScope._ = window._;
            });

        let body = document.getElementsByTagName("body")[0];
        angular.bootstrap(body, ['viator-bootstrap']);
    });