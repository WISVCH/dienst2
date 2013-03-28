// Generated by CoffeeScript 1.4.0
(function() {
  var addItem, format;

  format = function(date) {
    date.setHours(0, 0, 0);
    return date.getFullYear() + '-' + (date.getMonth() + 1) + '-' + date.getDate() + 'T00:00+00:00';
  };

  window.App = angular.module('post', ['post.controllers', 'typeahead']).config([
    '$routeProvider', function($routeProvider) {
      $routeProvider.when('/dashboard', {
        templateUrl: window.prefix + 'partials/post/dashboard.html',
        controller: 'DashboardController'
      });
      $routeProvider.when('/week', {
        templateUrl: window.prefix + 'partials/post/week.html',
        controller: 'WeekController'
      });
      $routeProvider.when('/av', {
        templateUrl: window.prefix + 'partials/post/av.html',
        controller: 'AVController'
      });
      $routeProvider.otherwise({
        redirectTo: '/dashboard'
      });
    }
  ]);

  addItem = {};

  angular.module('post.controllers', ['post.apiv2']).controller('DashboardController', [
    '$scope', 'Item', function($scope, Item) {
      var allItems;
      $scope.items = [];
      allItems = [];
      Item.all(function(items, meta) {
        return $scope.items = allItems = items;
      });
      addItem = function(item) {
        return $scope.items.push(item);
      };
      $scope.next = function() {
        return $scope.items.next(function(items) {
          return $scope.items = items;
        });
      };
      $scope.previous = function() {
        return $scope.items.previous(function(items) {
          return $scope.items = items;
        });
      };
      return $scope.$watch('search', function() {
        if ($scope.search.length > 1) {
          return Item.search($scope.search, function(items) {
            return $scope.items = items;
          });
        } else {
          return $scope.items = allItems;
        }
      });
    }
  ]).controller('FormController', [
    '$scope', 'Category', 'Source', 'Item', function($scope, Category, Source, Item) {
      angular.element("input[ng-model='description']").focus();
      $scope.categories = function(query, callback) {
        return Category.search(query, function(categories) {
          return callback(categories);
        });
      };
      $scope.sources = function(query, callback) {
        return Source.search(query, function(sources) {
          return callback(sources);
        });
      };
      return $scope.submit = function() {
        var item;
        if ($scope.sender && $scope.receiver && $scope.category && $scope.description) {
          item = new Item();
          item.sender = $scope.sender_model.resource_uri;
          item.receiver = $scope.receiver_model.resource_uri;
          item.category = $scope.category_model.resource_uri;
          item.description = $scope.description;
          return item.create(function(obj) {
            $scope.sender = "";
            $scope.receiver = "";
            $scope.category = "";
            $scope.description = "";
            addItem(obj);
            return angular.element("input[ng-model='description']").focus();
          });
        }
      };
    }
  ]).controller('WeekController', [
    '$scope', 'Item', function($scope, Item) {
      var addDays, today;
      $scope.items = [];
      addDays = function(date, days) {
        var next;
        next = new Date();
        next.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
        return next;
      };
      $scope.next = function() {
        return $scope.monday = addDays($scope.monday, 7);
      };
      $scope.previous = function() {
        return $scope.monday = addDays($scope.monday, -7);
      };
      today = new Date();
      $scope.monday = new Date(today - ((today.getDay() + 6) % 7) * 24 * 60 * 60 * 1000);
      return $scope.$watch('monday', function() {
        $scope.nextmonday = addDays($scope.monday, 7);
        return Item.between($scope.monday, $scope.nextmonday, function(items, meta) {
          return $scope.items = items;
        });
      });
    }
  ]).controller('AVController', [
    '$scope', 'Item', 'Category', function($scope, Item, Category) {
      var updateItems;
      $scope.categories = [];
      $scope.datefrom = new Date();
      Category.all(function(categories, meta) {
        $scope.categories = categories;
        return $scope.categories.forEach(function(category) {
          return category.items = [];
        });
      });
      $scope.$watch('avdate', function() {
        var matches;
        if ($scope.avdate && (matches = $scope.avdate.match(/(\d{1,2})-(\d{1,2})-(\d{4})/))) {
          $scope.datefrom.setFullYear(matches[3], matches[2] - 1, matches[1]);
          return updateItems();
        }
      });
      return updateItems = function() {
        return $scope.categories.forEach(function(category) {
          return Item._more({
            method: 'GET',
            url: Item.api_root,
            params: {
              'category': category.id,
              'limit': 0,
              'date__gte': format($scope.datefrom)
            }
          }, function(items, meta) {
            var counted;
            category.items = [];
            if (true) {
              counted = [];
              items.forEach(function(item) {
                var found;
                found = false;
                counted.forEach(function(citem) {
                  if (citem.description.toUpperCase() === item.description.toUpperCase() && citem.sendername === item.sendername) {
                    citem.count++;
                    return found = true;
                  }
                });
                if (found === false) {
                  item.count = 1;
                  return counted.push(item);
                }
              });
              category.items = counted;
            } else {
              category.items = items;
            }
            return console.log(category.items);
          });
        });
      };
    }
  ]);

  angular.module('post.apiv2', ['dienst2']).factory('Category', [
    'Tastypie', function(Tastypie) {
      var Category;
      Category = Tastypie('api/v2/category/');
      Category.prototype.toString = function() {
        return this.name;
      };
      return Category;
    }
  ]).factory('Source', [
    'Tastypie', function(Tastypie) {
      var Source;
      Source = Tastypie('api/v2/source/');
      Source.prototype.toString = function() {
        return this.name;
      };
      return Source;
    }
  ]).factory('Item', [
    'Tastypie', '$http', function(Tastypie, $http) {
      var Item;
      Item = Tastypie('api/v2/item/');
      Item.prototype.toString = function() {
        return this.description;
      };
      Item.between = function(datefrom, dateto, success) {
        return Item._more({
          method: 'GET',
          url: Item.api_root,
          params: {
            'limit': 0,
            'date__gte': format(datefrom),
            'date__lt': format(dateto)
          }
        }, success);
      };
      return Item;
    }
  ]);

}).call(this);