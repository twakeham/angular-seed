define([
    'angular',
    'modules/module.deps.js'
], function (angular) {
    'use strict';

    return angular

        .module('erp', [])

        .constant('api', 'http://127.0.0.1:8000/api/')

        .config(['$stateProvider', '$urlRouterProvider',
            function (stateProvider, urlRouterProvider) {
                $urlRouterProvider.otherwise("/login");
            }
        ]);

});