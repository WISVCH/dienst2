#
# Main Application
#

window.App = angular
  .module('kas', ['kas.controllers', 'typeahead'])
  .config(['$routeProvider', ($routeProvider) -> 
    $routeProvider.when('/transactions', {templateUrl: window.prefix + 'partials/kas/transactions.html', controller: 'TransactionController'})
    $routeProvider.when('/closures', {templateUrl: window.prefix + 'partials/kas/closures.html', controller: 'ClosureController'})
    $routeProvider.when('/closures/:closureID', {templateUrl: window.prefix + 'partials/kas/closure.html', controller: 'ClosureDetailController'})
    $routeProvider.when('/barcode', {templateUrl: window.prefix + 'partials/kas/barcode.html', controller: 'BarcodeController'})
    $routeProvider.otherwise({redirectTo: '/transactions'})
    return
  ])

#
# Controllers
#
addItem = {}

angular
  .module('kas.controllers', ['kas.apiv2', 'kas.barcode'])
  .controller('TransactionController', ['$scope', 'Transaction', ($scope, Transaction) -> 

    $scope.transactions = []
    Transaction.all((transactions, meta) -> $scope.transactions = transactions )

    addItem = (transaction) -> $scope.transactions.push(transaction)

    $scope.next = () ->
      $scope.transactions.next((transactions) -> $scope.transactions = transactions)

    $scope.previous = () ->
      $scope.transactions.previous((transactions) -> $scope.transactions = transactions)

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
    $scope.unfinished = false;
    Closure.unfinished((closure) -> 
      if closure.total_count == 1
        $scope.unfinished = closure[0]
    )

    $scope.closures = []
    Closure.all((closures) ->
      $scope.closures = closures
    )

    $('.extrainfo').popover({trigger:"focus", placement:"bottom", title:"Informatie"})
  ])
  .controller('ClosureFormController', ['$scope', '$location', 'Transaction', 'Closure', ($scope, $location, Transaction, Closure) -> 
    $scope.newclosure = () ->
      if $scope.in_cash
        transaction_cash = new Transaction()
        transaction_cash.amount = parseFloat($scope.in_cash.replace(',','.'))
        transaction_cash.method = "C"
        transaction_cash.description = "Kasinkomsten"
        transaction_cash.valid = true

        transaction_cash.create((obj) ->)

      if $scope.in_pin
        transaction_pin = new Transaction()
        transaction_pin.amount = parseFloat($scope.in_pin.replace(',','.'))
        transaction_pin.method = "P"
        transaction_pin.description = "Pininkomsten"
        transaction_pin.valid = true

        transaction_pin.create((obj) ->)

      closure = new Closure()
      closure.create((obj) ->
        $location.path('/closures/' + obj.id)
      )
  ])
  .controller('ClosureDetailController', ['$routeParams', '$scope', 'Transaction', 'Closure', ($routeParams, $scope, Transaction, Closure) -> 
    $scope.closure = false

    $scope.transactions = []

    Closure.get($routeParams.closureID, (closure) -> 
      $scope.closure = closure

      if not $scope.closure.finished
        # to make sure the latest transactions are processed
        $scope.closure.update((closure) ->
          $scope.closure = closure
        )

      $scope.loadTransactions()
    )

    $scope.loadTransactions = () ->
      Transaction.inClosure($scope.closure, (transactions) ->
        $scope.transactions = transactions
      )

    $scope.save = () ->
      $scope.closure.update((closure) ->
        $scope.loadTransactions() # Reload transactions
        $scope.closure = closure
        if ($scope.closure.cashdifference == 0 and $scope.closure.pindifference == 0) or $scope.confirmed

          $scope.closure.finished = true
          $scope.closure.update((closure) -> 
            $scope.confirmed = $scope.problem = false
            alert("Dagafsluiting voltooid.")
          )
        else
          $scope.problem = true
      )

    $scope.confirm = () ->
      $scope.confirmed = true
      $scope.save()

    $scope.$watch(
      "closure.num_e500 + closure.num_e200 + closure.num_e100 + closure.num_e50 + closure.num_e20 + closure.num_e10 + closure.num_e5 + closure.num_e2 + closure.num_e1 + closure.num_e050 + closure.num_e020 + closure.num_e010 + closure.num_e005"
      () ->
        $scope.closure.total = 500 * $scope.closure.num_e500 + 200 * $scope.closure.num_e200 + 100 * $scope.closure.num_e100 + 50 * $scope.closure.num_e50 + 20 * $scope.closure.num_e20 + 10 * $scope.closure.num_e10 + 5 * $scope.closure.num_e5 + 2 * $scope.closure.num_e2 + 1 * $scope.closure.num_e1 + 0.5 * $scope.closure.num_e050 + 0.2 * $scope.closure.num_e020 + 0.1 * $scope.closure.num_e010 + 0.05 * $scope.closure.num_e005
    )

    $scope.$watch('closure.total - closure.previoustotal - closure.transactions_cash', () ->
      cashdifference = $scope.closure.total - $scope.closure.previoustotal - $scope.closure.transactions_cash
      $scope.closure.cashdifference = Math.round(cashdifference*100)/100
    )

    $(document).delegate('input.input-mini', 'keyup', () -> $scope.$digest())
  ])
  .controller('BarcodeController', ['$scope', 'Barcode', ($scope, Barcode) -> 
    $scope.images = []

    canvas = $('#canvas')[0]
    context = canvas.getContext('2d')

    width = $(canvas).attr('width')
    height = $(canvas).attr('height')

    if window.devicePixelRatio
      $(canvas).attr('width', width * window.devicePixelRatio)
      $(canvas).attr('height', height * window.devicePixelRatio)
      $(canvas).css('width', width)
      $(canvas).css('height', height)
      context.scale(window.devicePixelRatio, window.devicePixelRatio)

    ocanvas = oCanvas.create({canvas: "#canvas"})

    $scope.$watch('barcode + description', () ->
      if $scope.barcode && $scope.barcode % 1 == 0
        Barcode.create($scope.barcode, $scope.description).draw(ocanvas)
    )

    $scope.getImage = () ->
      $scope.images.push(ocanvas.canvasElement.toDataURL("image/png"))

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
      if this.editable
        this.valid = if this.valid then false else true
        this.update()
    
    Transaction.inClosure = (closure, success) -> 
      params = {'limit': 0, 'date__lte':closure.date}

      if closure.previousdate
        params.date__gt = closure.previousdate

      Transaction._more({ method: 'GET', url: Transaction.api_root , params: params }, success)

    Transaction
  ])
  .factory('Closure', ['Tastypie', (Tastypie) ->
    Closure = Tastypie('api/v2/closure/')
    Closure.prototype.toString = () -> this.date
    Closure.unfinished = (success) -> Closure._more({ method: 'GET', url: Closure.api_root , params: {'finished': false} }, success)
    Closure
  ])