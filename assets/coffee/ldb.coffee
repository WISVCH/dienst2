#
# Helpers
#

getid = (uri) -> 
  try
    parts = uri.split( '/' )
    return parts[parts.length-2]
  catch e
    return undefined
#
# Main Application
#

window.App = angular
  .module('ldb', ['ldb.controllers', 'typeahead', 'dienst2.forms'])
  .config(['$routeProvider', ($routeProvider) -> 
    $routeProvider.when('/dashboard', {templateUrl: window.prefix + 'partials/ldb/dashboard.html', controller: 'DashboardController'})
    $routeProvider.when('/person/new', {templateUrl: window.prefix + 'partials/ldb/person.html', controller: 'PersonDetailController'})
    $routeProvider.when('/person/:personID', {templateUrl: window.prefix + 'partials/ldb/person.html', controller: 'PersonDetailController'})
    $routeProvider.when('/organization/new', {templateUrl: window.prefix + 'partials/ldb/organization.html', controller: 'OrganizationDetailController'})
    $routeProvider.when('/organization/:organizationID', {templateUrl: window.prefix + 'partials/ldb/organization.html', controller: 'OrganizationDetailController'})
    $routeProvider.when('/committees', {templateUrl: window.prefix + 'partials/ldb/committees.html', controller: 'CommitteeController'})
    $routeProvider.when('/export', {templateUrl: window.prefix + 'partials/ldb/export.html', controller: 'ExportController'})
    $routeProvider.otherwise({redirectTo: '/dashboard'})
    return
  ])

#
# Controllers
#

angular
  .module('ldb.controllers', ['ldb.apiv2'])
  .controller('DashboardController', ['$scope', 'Person', 'Organization', ($scope, Person, Organization) -> 

    $scope.search = ""
    $scope.searchtype = "p"
    $scope.results = []

    classes = {o: Organization, p: Person}

    searchID = 0
    $scope.$watch('searchtype + search', () ->
      if $scope.search.length > 1
        searchID++
        classes[$scope.searchtype].search(
          $scope.search
          (results, status, headers, config) -> 
            if config.params.searchID == searchID
              $scope.results = results
          'start'
          searchID
        )
      else
        $scope.results = []
    )

    $("#zoekbalk").focus()
  ])
  .controller('PersonDetailController', ['$routeParams', '$location', '$scope', 'Person', 'Committee', 'CommitteeMembership', 'country_list', ($routeParams, $location, $scope, Person, Committee, CommitteeMembership, country_list) -> 
    
    # Setup

    $scope.country_list = country_list
    $scope.editmode = $routeParams.editmode == 'on'
    $scope.admin = window.admin

    $scope.$watch('editmode', () ->
      if $scope.editmode
        $location.search('editmode', 'on')
      else if $routeParams.editmode
        $location.search('editmode', 'off')
    )

    # All committees

    $scope.committeelist = []
    Committee.all((committeelist) ->
      $scope.committeelist = committeelist
    )

    # Committee Memberships

    $scope.committeeFilter = (committee) -> return !committee._delete  

    # Person search (for living with)

    $scope.otherpersons = (query, callback) -> 
      Person.search(
        query
        (sources) -> 
          callback(sources)
        'start'
      )

    $scope.notLivingWith = () ->
      $scope.living_with_model = null
      $scope.living_with = null
      $scope.person.living_with_model = null
      $scope.person.living_with = null

    $scope.$watch('living_with_model', ()->
      model = $scope.living_with_model
      if model && model.resource_uri
        $scope.person.living_with_model = model
        $scope.person.living_with = model.resource_uri

    )

    # Save function

    $scope.save = () ->
      $scope.person.saveAll(
        (success) -> 
          $location.path('/person/' + $scope.person.id)
      )
      $scope.editmode = false

    $scope.removePerson = () ->
      $scope.person.remove(() ->
        alert "Removed person."
        $location.path('/dashboard')
      )

    # Loading everything
    if $routeParams.personID
      Person.get($routeParams.personID, (person) -> 
        $scope.person = person
        $scope.person.loadSubresources()
      )
    else
      $scope.person = new Person()
      $scope.person.loadSubresources()
      $scope.editmode = true
  ])
  .controller('OrganizationDetailController', ['$routeParams', '$location', '$scope', 'Organization', 'country_list', ($routeParams, $location, $scope, Organization, country_list) -> 
    
    # Setup

    $scope.country_list = country_list
    $scope.editmode = $routeParams.editmode == 'on'
    $scope.admin = window.admin

    $scope.$watch('editmode', () ->
      if $scope.editmode
        $location.search('editmode', 'on')
      else if $routeParams.editmode
        $location.search('editmode', 'off')
    )

    # Save function

    $scope.save = () ->
      $scope.organization.save(
        (success) -> $location.path('/organization/' + $scope.organization.id)
      )
      $scope.editmode = false

    $scope.removeOrganization = () ->
      $scope.organization.remove(() ->
        alert "Removed organization"
        $location.path('/dashboard')
      )

    # Loading everything
    if $routeParams.organizationID
      Organization.get($routeParams.organizationID, (organization) -> 
        $scope.organization = organization
      )
    else
      $scope.organization = new Organization()
      $scope.editmode = true
  ])
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
  .controller('CommitteeController', ['$scope', 'Committee', 'CommitteeMembership', ($scope, Committee, CommitteeMembership) ->
    # All committees

    $scope.committeelist = []
    Committee.all((committeelist) ->
      $scope.committeelist = committeelist
    )

    # Search

    $scope.search = {
      board: undefined
      committee: undefined
    }

    search = {}
    $scope.$watch(
      'search'
      ()->
        search = {'limit': 0}
        if $scope.search.board
          search['board'] = $scope.search.board
        if $scope.search.committee
          search['committee'] = getid($scope.search.committee)
      true
    )

    $scope.withCommittee = (committee) ->
      $scope.search['committee'] = committee
      search['committee'] = getid(committee)
      $scope.load()

    $scope.getid = getid

    $scope.loading = false;
    $scope.load = () ->
      if !$scope.loading && (search.board || search.committee)
        $scope.loading = true
        CommitteeMembership._more(
          { method: 'GET', url: CommitteeMembership.api_root , params: search, cache: true }
          (committeememberships) ->
            $scope.loading = false
            $scope.committeememberships = committeememberships
        )

  ])

#
# API Helpers
#
emptyAddr = () -> 
  this.street_name = this.house_number = this.address_2 = this.address_3 = this.postcode = this.city = this.country = ""

#
# API Functions
#

angular
  .module('ldb.apiv2', ['dienst2'])
  .factory('Member', ['Tastypie', (Tastypie) -> Member = Tastypie('api/v2/member/')])
  .factory('Student', ['Tastypie', '$filter', (Tastypie, $filter) -> 
    Student = Tastypie('api/v2/student/')
    Student.prototype.confirm = () ->
      today = new Date()
      datefilter = $filter('date')
      this.date_verified = datefilter(today, 'yyyy-MM-dd')
      if this.resource_uri
        this.update()
    Student
  ])
  .factory('Alumnus', ['Tastypie', (Tastypie) -> Alumnus = Tastypie('api/v2/alumnus/')])
  .factory('Employee', ['Tastypie', (Tastypie) -> Employee = Tastypie('api/v2/employee/')])
  .factory('CommitteeMembership', ['Tastypie', (Tastypie) -> CommitteeMembership = Tastypie('api/v2/committeeMembership/')])

  .factory('Person', ['Tastypie', 'Member', 'Student', 'Alumnus', 'Employee', 'CommitteeMembership', (Tastypie, Member, Student, Alumnus, Employee, CommitteeMembership) -> 
    Person = Tastypie('api/v2/person/')
    
    Person.prototype.emptyAddr = emptyAddr

    Person.prototype.toString = () -> 
      name = this.firstname
      if this.preposition
        name += " " + this.preposition 
      name += " " + this.surname
      name

    Person.prototype.committeememberships = []
    
    Person.prototype.loadSubresources = (success) -> 

      update = () ->
        if success
          success()

      self = this
      
      Student.getSubresource(self.student, (student) -> 
        student = new Student() if !student
        self.student_model = student
        update()
      )

      Member.getSubresource(self.member, (member) -> 
        member = new Member() if !member
        self.member_model = member
        update()
      )

      Alumnus.getSubresource(self.alumnus, (alumnus) -> 
        alumnus = new Alumnus() if !alumnus
        self.alumnus_model = alumnus
        update()
      )

      Employee.getSubresource(self.employee, (employee) -> 
        employee = new Employee() if !employee
        self.employee_model = employee
        update()
      )

      Person.getSubresource(self.living_with, (person) -> 
        self.living_with_model = person
        update()
      )

      if self.committees
        CommitteeMembership._more({ method: 'GET', url: CommitteeMembership.api_root , params: {'limit': 0, 'person':self.id} }, (committeememberships) ->
          self.committeememberships = committeememberships
          update()
        )
    
    Person.prototype.newCommittee = () ->
      committeemembership = new CommitteeMembership()
      committeemembership.person = this.resource_uri
      this.committeememberships.push(committeemembership)

    Person.prototype.saveAll = (success, error) ->
      handleError = error

      if this.living_with_model
        this.living_with = this.living_with_model.resource_uri

      this.student_model.save(undefined, alert)
      this.member_model.save(undefined, alert)
      this.alumnus_model.save(undefined, alert)
      this.employee_model.save(undefined, alert)

      angular.forEach(this.committeememberships, (obj) ->
        obj.save(undefined, alert)
      )

      this.save(success, alert)

    Person
  ])
  .factory('Organization', ['Tastypie', (Tastypie) -> 
    Organization = Tastypie('api/v2/organization/')
    Organization.prototype.emptyAddr = emptyAddr
    Organization
  ])
  .factory('Committee', ['Tastypie', (Tastypie) ->
    Committee = Tastypie('api/v2/committee/')
    Committee.prototype.toString = () -> this.committeename
    Committee.all = (success) -> Committee._more({ method: 'GET', url: Committee.api_root , params: {'limit': 0}, cache: true }, success)
    Committee
  ])
