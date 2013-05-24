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

    $scope.$watch('searchtype + search', () ->
      if $scope.search.length > 1
        classes[$scope.searchtype].search(
          $scope.search
          (results) -> 
            $scope.results = results
          'start'
        )
      else
        $scope.results = []
    )

    $("#zoekbalk").focus()
  ])
  .controller('PersonDetailController', ['$routeParams', '$location', '$scope', 'Person', 'Committee', 'CommitteeMembership', 'country_list', ($routeParams, $location, $scope, Person, Committee, CommitteeMembership, country_list) -> 
    
    # Setup

    $scope.country_list = country_list
    $scope.editmode = false

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
        (success) -> $location.path('/person/' + $scope.person.id)
        (data, status, headers, config) ->
          if status == 400
            alert "Het formulier is niet geldig. \n \n" + angular.toJson(data)
            $scope.editmode = true
        )
      $scope.editmode = false

    $scope.removePerson = () ->
      $scope.person.remove(() ->
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
    $scope.editmode = false

    # Save function

    $scope.save = () ->
      $scope.organization.save(
        (success) -> $location.path('/organization/' + $scope.organization.id)
        (data, status, headers, config) ->
          if status == 400
            alert "Het formulier is niet geldig. \n \n" + angular.toJson(data)
            $scope.editmode = true
        )
      $scope.editmode = false

    $scope.removeOrganization = () ->
      $scope.organization.remove(() ->
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
  .controller('ExportController', ['$scope', ($scope) ->
  ])

#
# API Helpers
#
emptyAddr = () -> 
  this.street_name = this.house_number = this.address_2 = this.address_3 = this.postcode = this.city = this.country = null

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

    handleError = () ->

    process = (obj, success, handleError) ->
      if obj.changed()
        if obj.resource_uri
          if obj._delete
            obj.remove(success, handleError)
          else
            obj.update(success, handleError)
        else
          obj.create(success, handleError)
    
    Person.prototype.newCommittee = () ->
      committeemembership = new CommitteeMembership()
      committeemembership.person = this.resource_uri
      this.committeememberships.push(committeemembership)

    Person.prototype.saveAll = (success, error) ->
      handleError = error

      if this.living_with_model
        this.living_with = this.living_with_model.resource_uri

      process(this.student_model)
      process(this.member_model)
      process(this.alumnus_model)
      process(this.employee_model)

      angular.forEach(this.committeememberships, (obj) ->
        process(obj)
      )

      process(this, ()-> success)

    Person
  ])
  .factory('Organization', ['Tastypie', (Tastypie) -> 
    Organization = Tastypie('api/v2/organization/')
    Organization.prototype.emptyAddr = emptyAddr
    Organization.prototype.save = (success, error) ->
      if this.changed()
        if this.resource_uri
          if this._delete
            this.remove(success, error)
          else
            this.update(success, error)
        else
          this.create(success, error)
    Organization
  ])
  .factory('Committee', ['Tastypie', (Tastypie) ->
    Committee = Tastypie('api/v2/committee/')
    Committee.prototype.toString = () -> this.committeename
    Committee.all = (success) -> Committee._more({ method: 'GET', url: Committee.api_root , params: {'limit': 0} }, success)
    Committee
  ])
  
  