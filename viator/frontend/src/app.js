// Load libraries
import angular from 'angular';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';

import SearchController from 'src/controllers/SearchController';
import SearchResultsController from 'src/controllers/SearchResultsController';
import PostDataService from 'src/services/PostDataService';
import URL from 'src/constants/URL';
import EVENTS from 'src/constants/EVENTS';

export default angular.module('viator-app', ['ngMaterial'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('orange')
            .accentPalette('light-green');
    })
    .constant('URL', URL)
    .constant('EVENTS', EVENTS)
    .controller('SearchController', SearchController)
    .controller('SearchResultsController', SearchResultsController)
    .service('PostDataService', PostDataService)