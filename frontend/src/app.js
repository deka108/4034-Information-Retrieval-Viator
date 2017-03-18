// Load libraries
import angular from 'angular';
import _ from 'lodash';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';
import 'angular-material-data-table';
import 'angular-utils-pagination';
import 'angular-busy';

import SearchController from 'src/controllers/SearchController';
import AdminController from 'src/controllers/AdminController';
import InitializationService from 'src/services/InitializationService';
import DbDataService from 'src/services/DbDataService';
import SearchDataService from 'src/services/SearchDataService';
import SolrDataService from 'src/services/SolrDataService';
import URL from 'src/constants/URL';
import EVENTS from 'src/constants/EVENTS';

export default angular.module('viator-app', ['ngMaterial', 'md.data.table', 'angularUtils.directives.dirPagination', 'cgBusy', 'ngAnimate'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('blue')
            .accentPalette('light-green');
    })
    .constant('URL', URL)
    .constant('EVENTS', EVENTS)
    .constant('_', _)
    .controller('SearchController', SearchController)
    .controller('AdminController', AdminController)
    .service('SearchDataService', SearchDataService)
    .service('DbDataService', DbDataService)
    .service('InitializationService', InitializationService)
    .service('SolrDataService', SolrDataService)