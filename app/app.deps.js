require.config(
    {
        paths: {
            'angular': 'lib/angular/angular',
            'angularUiRouter': 'lib/angular-ui-router/release/angular-ui-router'
        },
        shim: {
            'angular': {
                exports: 'angular'
            },
            'angularUiRouter': {
                deps: ['angular']
            }
        }
    }
);

require(
    [
        'angular',
        'app'
    ], function (angular, app) {
        'use strict';

        angular.element(document).ready(function angularBootstrapInit() {
            angular.bootstrap(document, ['erp']);
        })
    }
);