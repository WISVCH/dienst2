# Main Application
#

window.App = angular
  .module('ldb', ['ldb.controllers', 'dienst2.forms'])
  .config(['$routeProvider', ($routeProvider) ->
    $routeProvider.when('/export', {templateUrl: window.prefix + 'partials/ldb/export.html', controller: 'ExportController'})
    $routeProvider.otherwise({redirectTo: '/dashboard'})
    return
  ])

#
# Controllers
#

angular
  .module('ldb.controllers', [])
  .controller('ExportController', ['$scope', '$http', '$filter', ($scope, $http, $filter) ->

    $scope.export = {
      'queryset': {},
      'filters': {},
      'fields': {},
      'limit': 5000,
      'format': 'csv'
    }

    $scope.loading = false

    $scope.loadExport = () ->
      $scope.loading = true
      $http({ method: 'GET', url: 'api/v2/export/', params: $scope.export })
        .success((data, status, headers, config) ->
          $scope.loading = false
          $scope.data = data
        )
        .error(() ->
          $scope.loading = false
          $scope.data = "FOUT"
        )
  ])
