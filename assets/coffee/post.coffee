#
# Helper Functions
#

format = (date) -> 
  date.setHours(0,0,0)
  date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + 'T00:00+00:00'

#
# Main Application
#

window.App = angular
  .module('post', ['post.controllers', 'typeahead'])
  .config(['$routeProvider', ($routeProvider) -> 
    $routeProvider.when('/dashboard', {templateUrl: window.prefix + 'partials/post/dashboard.html', controller: 'DashboardController'})
    $routeProvider.when('/week', {templateUrl: window.prefix + 'partials/post/week.html', controller: 'WeekController'})
    $routeProvider.when('/av', {templateUrl: window.prefix + 'partials/post/av.html', controller: 'AVController'})
    $routeProvider.otherwise({redirectTo: '/dashboard'})
    return
  ])

#
# Controllers
#

addItem = {};

angular
  .module('post.controllers', ['post.apiv2'])
  .controller('DashboardController', ['$scope', 'Item', ($scope, Item) -> 
    $scope.items = []
    allItems = []
    Item.all((items, meta) -> $scope.items = allItems = items)
    addItem = (item) -> $scope.items.push(item)

    $scope.next = () ->
      $scope.items.next((items) -> $scope.items = items)

    $scope.previous = () ->
      $scope.items.previous((items) -> $scope.items = items)

    $scope.$watch('search', () ->
      if $scope.search.length > 1
        Item.search($scope.search, (items) -> 
          $scope.items = items
        )
      else
        $scope.items = allItems
    )

  ])
  .controller('FormController', ['$scope', 'Category', 'Source', 'Item', ($scope, Category, Source, Item) -> 
    angular.element("input[ng-model='description']").focus()
    $scope.categories = (query, callback) -> 
      Category.search(query, (categories) -> 
        callback(categories)
      )
    $scope.sources = (query, callback) -> 
      Source.search(query, (sources) -> 
        callback(sources)
      )
    $scope.submit = () ->
      if $scope.sender and $scope.receiver and $scope.category and $scope.description
        item = new Item()
        item.sender = $scope.sender_model.resource_uri
        item.receiver = $scope.receiver_model.resource_uri
        item.category = $scope.category_model.resource_uri
        item.description = $scope.description

        item.create((obj) -> 
          $scope.sender = ""
          $scope.receiver = ""
          $scope.category = ""
          $scope.description = ""
          addItem(obj)
          angular.element("input[ng-model='description']").focus()
        )
  ])
  .controller('WeekController', ['$scope', 'Item', ($scope, Item) ->
    $scope.items = []

    addDays = (date, days) -> 
      next = new Date()
      next.setTime(date.getTime() + days * 24*60*60*1000)
      next

    $scope.next = () ->
      $scope.monday = addDays($scope.monday, 7)

    $scope.previous = () ->
      $scope.monday = addDays($scope.monday, -7)

    today = new Date()
    $scope.monday = new Date(today - ((today.getDay() + 6) % 7) * 24*60*60*1000)

    $scope.$watch('monday', () ->
      $scope.nextmonday = addDays($scope.monday, 7)
      Item.between($scope.monday, $scope.nextmonday, (items, meta) -> 
        $scope.items = items
      )
    )
  ])
  .controller('AVController', ['$scope', 'Item', 'Category', ($scope, Item, Category) ->
    $scope.categories = []

    $scope.datefrom = new Date()

    Category.all((categories, meta) -> 
      $scope.categories = categories
      $scope.categories.forEach((category) -> category.items = [])
    )

    $scope.$watch('avdate', () ->
      if $scope.avdate and matches = $scope.avdate.match(/(\d{1,2})-(\d{1,2})-(\d{4})/)
        $scope.datefrom.setFullYear(matches[3],matches[2]-1,matches[1])
        updateItems()
    )

    updateItems = () ->
      $scope.categories.forEach((category) ->
        Item._more({ method: 'GET', url: Item.api_root , params: {'category': category.id,'limit': 0, 'date__gte':format($scope.datefrom)}}, (items, meta) ->
          category.items = []
          if true
            counted = []
            items.forEach((item) ->
              found = false
              counted.forEach((citem) ->
                if citem.description.toUpperCase() == item.description.toUpperCase() and citem.sendername == item.sendername
                  citem.count++
                  found = true
              )
              if found == false
                item.count = 1
                counted.push(item)
            )
            
            category.items = counted
          else
            category.items = items

          console.log category.items
        )
      )
  ])

#
# API Functions
#

angular
  .module('post.apiv2', ['dienst2'])
  .factory('Category', ['Tastypie', (Tastypie) ->
    Category = Tastypie('api/v2/category/')
    Category.prototype.toString = () -> this.name
    Category
  ])
  .factory('Source', ['Tastypie', (Tastypie) ->
    Source = Tastypie('api/v2/source/')
    Source.prototype.toString = () -> this.name
    Source
  ])
  .factory('Item', ['Tastypie', '$http', (Tastypie, $http) ->
    Item = Tastypie('api/v2/item/')
    Item.prototype.toString = () -> this.description
    Item.between = (datefrom, dateto, success) -> 
      Item._more({ method: 'GET', url: Item.api_root , params: {'limit': 0, 'date__gte':format(datefrom), 'date__lt':format(dateto)} }, success)
    Item
  ])