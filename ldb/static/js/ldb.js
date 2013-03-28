// Generated by CoffeeScript 1.4.0
(function() {

  window.App = angular.module('ldb', ['ldb.controllers', 'typeahead']).config([
    '$routeProvider', function($routeProvider) {
      $routeProvider.when('/dashboard', {
        templateUrl: window.prefix + 'partials/ldb/dashboard.html',
        controller: 'DashboardController'
      });
      $routeProvider.when('/person/:personID', {
        templateUrl: window.prefix + 'partials/ldb/person.html',
        controller: 'PersonDetailController'
      });
      $routeProvider.otherwise({
        redirectTo: '/dashboard'
      });
    }
  ]);

  angular.module('ldb.controllers', ['ldb.apiv2']).controller('DashboardController', [
    '$scope', 'Person', function($scope, Person) {
      $scope.search = "";
      $scope.people = [];
      return $scope.$watch('search', function() {
        if ($scope.search.length > 1) {
          return Person.search($scope.search, function(people) {
            return $scope.people = people;
          });
        } else {
          return $scope.people = [];
        }
      });
    }
  ]).controller('PersonDetailController', [
    '$routeParams', '$scope', 'Person', function($routeParams, $scope, Person) {
      $scope.person = false;
      $scope.member = false;
      $scope.student = false;
      $scope.alumnus = false;
      $scope.employee = false;
      $scope.committees = [];
      return Person.get($routeParams.personID, function(person) {
        console.log(person);
        $scope.person = person;
        if (person.member) {
          person.getSubresource(person.member, function(member) {
            return $scope.member = member;
          });
        }
        if (person.student) {
          person.getSubresource(person.student, function(student) {
            return $scope.student = student;
          });
        }
        if (person.alumnus) {
          person.getSubresource(person.alumnus, function(alumnus) {
            return $scope.alumnus = alumnus;
          });
        }
        if (person.employee) {
          person.getSubresource(person.employee, function(employee) {
            return $scope.employee = employee;
          });
        }
        if (person.committees) {
          return angular.forEach(person.committees, function(committee) {
            return person.getSubresource(committee, function(committee) {
              return $scope.committees.push(committee);
            });
          });
        }
      });
    }
  ]);

  angular.module('ldb.apiv2', ['dienst2']).factory('Person', [
    'Tastypie', function(Tastypie) {
      var Person;
      Person = Tastypie('api/v2/person/');
      Person.prototype.toString = function() {
        var name;
        name = self.firstname;
        if (self.preposition) {
          name += this.preposition;
        }
        name += this.surname;
        return name;
      };
      Person.prototype.getSubresource = function(url, success) {
        return Person._one({
          method: 'GET',
          url: url
        }, success);
      };
      return Person;
    }
  ]);

}).call(this);