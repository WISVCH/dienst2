(function() {
  // Main Application

  window.App = angular.module("ldb", ["ldb.controllers"]).config([
    "$routeProvider",
    function($routeProvider) {
      $routeProvider.when("/", {
        templateUrl: window.partialUrl,
        controller: "ExportController"
      });
    }
  ]);

  // Controllers
  angular.module("ldb.controllers", []).controller("ExportController", [
    "$scope",
    "$http",
    "$filter",
    function($scope, $http, $filter) {
      $scope.export = {
        queryset: {},
        filters: {},
        fields: {},
        limit: 5000,
        format: "csv"
      };
      $scope.loading = false;
      return ($scope.loadExport = function() {
        $scope.loading = true;
        return $http({
          method: "GET",
          url: window.apiUrl,
          params: $scope.export
        })
          .success(function(data, status, headers, config) {
            $scope.loading = false;
            return ($scope.data = data);
          })
          .error(function(err) {
            $scope.loading = false;
            console.error(err);
            return ($scope.data = err);
          });
      });
    }
  ]);
}.call(this));
