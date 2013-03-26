#
# Main Application
#

window.App = angular
  .module('kas', ['kas.controllers', 'typeahead'])
  .config(['$routeProvider', ($routeProvider) -> 
    $routeProvider.when('/transactions', {templateUrl: window.prefix + 'partials/kas/transactions.html', controller: 'TransactionController'})
    $routeProvider.when('/closures', {templateUrl: window.prefix + 'partials/kas/closures.html', controller: 'ClosureController'})
    $routeProvider.when('/closures/:closureID', {templateUrl: window.prefix + 'partials/kas/closure.html', controller: 'ClosureDetailController'})
    $routeProvider.otherwise({redirectTo: '/transactions'})
    return
  ])

#
# Controllers
#
addItem = {}

angular
  .module('kas.controllers', ['kas.apiv2'])
  .controller('TransactionController', ['$scope', 'Transaction', ($scope, Transaction) -> 

    $scope.transactions = []
    Transaction.all((transactions, meta) -> $scope.transactions = transactions )

    addItem = (transaction) -> $scope.transactions.push(transaction)

    $scope.next = () ->
      $scope.transactions.next((items) -> $scope.items = items)

    $scope.previous = () ->
      $scope.transactions.previous((items) -> $scope.items = items)

  ])
  .controller('TransactionFormController', ['$scope', 'Transaction', ($scope, Transaction) -> 
    angular.element("input[ng-model='amount']").focus()

    $scope.inout = "OUT"
    $scope.toggleInout = () ->
      $scope.inout = if $scope.inout == "OUT" then "IN" else "OUT"
      if $scope.inout == "OUT"
        $scope.method = "CASH"

    $scope.method = "CASH"
    $scope.toggleMethod = () ->
      $scope.method = if $scope.method == "CASH" then "PIN" else "CASH"
      if $scope.method == "PIN"
        $scope.inout = "IN"

    $scope.submit = () ->
      if $scope.amount and $scope.description
        transaction = new Transaction()

        transaction.amount = Math.abs(parseFloat($scope.amount.replace(',','.')))
        
        transaction.amount *= -1 if $scope.inout == "OUT"

        transaction.method = if $scope.method == "CASH" then "C" else "P"

        transaction.description = $scope.description

        transaction.valid = true

        console.log transaction

        transaction.create((obj) -> 
          $scope.inout = "OUT"
          $scope.method = "CASH"
          $scope.amount = ""
          $scope.description = ""
          addItem(obj)
          angular.element("input[ng-model='amount']").focus()
        )
  ])
  .controller('ClosureController', ['$scope', 'Transaction', 'Closure', ($scope, Transaction, Closure) -> 

    $scope.closures = []
    Closure.all((closures, meta) ->
      $scope.closures = closures
    )

  ])

#
# API Functions
#

angular
  .module('kas.apiv2', ['dienst2'])
  .factory('Transaction', ['Tastypie', (Tastypie) ->
    Transaction = Tastypie('api/v2/transaction/')
    Transaction.prototype.toString = () -> this.description
    Transaction.prototype.toggleValid = () -> 
      this.valid = if this.valid then false else true
      this.update()
    Transaction
  ])
  .factory('Closure', ['Tastypie', (Tastypie) ->
    Closure = Tastypie('api/v2/closure/')
    Closure.prototype.toString = () -> this.date
    Closure
  ])