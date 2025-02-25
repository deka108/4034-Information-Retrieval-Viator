// Load libraries
import angular from 'angular';
import _ from 'lodash';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';
import 'angular-material-data-table';
import 'angular-utils-pagination';
import 'angular-busy';
import 'angular-sanitize';
import 'angular-material/angular-material.min.css!';
import 'angular-busy/dist/angular-busy.min.css!';
import 'angular-material-data-table/dist/md-data-table.min.css!';
import 'style/app.css!';

import SearchController from 'src/controllers/SearchController';
import AdminController from 'src/controllers/AdminController';
import InitializationService from 'src/services/InitializationService';
import DbDataService from 'src/services/DbDataService';
import SearchDataService from 'src/services/SearchDataService';
import SolrDataService from 'src/services/SolrDataService';
import URL from 'src/constants/URL';
import EVENTS from 'src/constants/EVENTS';

export default angular.module('viator-app', ['ngMaterial', 'md.data.table', 'angularUtils.directives.dirPagination', 'cgBusy', 'ngAnimate', 'ngSanitize'])
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