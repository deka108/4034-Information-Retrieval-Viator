// Load libraries
import angular from 'angular';
import _ from 'lodash';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';
import 'angular-material-data-table';


import SearchController from 'src/controllers/SearchController';
import AdminController from 'src/controllers/AdminController';
import PostDataService from 'src/services/PostDataService';
import URL from 'src/constants/URL';
import EVENTS from 'src/constants/EVENTS';

export default angular.module('viator-app', ['ngMaterial', 'md.data.table'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('orange')
            .accentPalette('light-green');
    })
    .constant('URL', URL)
    .constant('EVENTS', EVENTS)
    .constant('_', _)
    .controller('SearchController', SearchController)
    .controller('AdminController', AdminController)
    .service('PostDataService', PostDataService)