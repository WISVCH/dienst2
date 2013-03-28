#
# Main Application
#

window.App = angular
  .module('ldb', ['ldb.controllers', 'typeahead'])
  .config(['$routeProvider', ($routeProvider) -> 
    $routeProvider.when('/dashboard', {templateUrl: window.prefix + 'partials/ldb/dashboard.html', controller: 'DashboardController'})
    $routeProvider.when('/person/:personID', {templateUrl: window.prefix + 'partials/ldb/person.html', controller: 'PersonDetailController'})
    $routeProvider.otherwise({redirectTo: '/dashboard'})
    return
  ])

#
# Controllers
#

angular
  .module('ldb.controllers', ['ldb.apiv2'])
  .controller('DashboardController', ['$scope', 'Person', ($scope, Person) -> 

    $scope.search = ""
    $scope.people = []

    $scope.$watch('search', () ->
      if $scope.search.length > 1
        Person.search($scope.search, (people) -> 
          $scope.people = people
        )
      else
        $scope.people = []
    )
  ])
  .controller('PersonDetailController', ['$routeParams', '$scope', 'Person', ($routeParams, $scope, Person) -> 
    $scope.person = false
    $scope.member = false
    $scope.student = false
    $scope.alumnus = false
    $scope.employee = false
    $scope.committees = []

    Person.get($routeParams.personID, (person) -> 

      console.log person

      $scope.person = person
      if person.member
        Person.getSubresource(person.member, (member) -> $scope.member = member)
      if person.student
        Person.getSubresource(person.student, (student) -> $scope.student = student)
      if person.alumnus
        Person.getSubresource(person.alumnus, (alumnus) -> $scope.alumnus = alumnus)
      if person.employee
        Person.getSubresource(person.employee, (employee) -> $scope.employee = employee)
      if person.committees
        angular.forEach(person.committees, (committee) -> 
          Person.getSubresource(committee, (committee) -> $scope.committees.push(committee))
        )
      
    )
  ])

#
# API Functions
#

angular
  .module('ldb.apiv2', ['dienst2'])
  .factory('Person', ['Tastypie', (Tastypie) ->
    Person = Tastypie('api/v2/person/')
    Person.prototype.toString = () -> 
      name = self.firstname
      if self.preposition
        name += this.preposition 
      name += this.surname
      name

    Person
  ])
  