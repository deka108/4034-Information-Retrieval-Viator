// Load libraries
import angular from 'angular';

import 'angular-animate';
import 'angular-aria';
import 'angular-material';

import SearchController from 'src/controllers/SearchController';
import URL from 'src/constants/URL';

export default angular.module('viator-app', ['ngMaterial'])
    .config(function($mdThemingProvider) {
        $mdThemingProvider.theme('default')
            .primaryPalette('orange')
            .accentPalette('light-green');
    })
    .constant('URL', URL)
    .controller('SearchController', SearchController);