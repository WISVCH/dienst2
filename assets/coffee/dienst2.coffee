$ = window.jQuery

angular.module('dienst2', [])
  .factory('Tastypie', ['$http', '$rootScope', ($http, $rootScope) ->
    
    throwError = (data, status, headers, config) ->
      alert("Server communication failed.")
      throw { message: 'Server communication failed.', status: status, config: config }

    report = (callback) ->
      return if callback then callback else throwError

    Tastypie = (api_root) -> 

      # Response Processors

      process = (data) -> 
        return new Model(data)

      processAll = (data) ->
        models = []
        angular.forEach(data.objects, (data) -> models.push(new Model(data)))

        if data.meta
          next = (success) -> 
            $http({ method: 'GET', url: data.meta.next })
              .error(report())
              .success((data, status, headers, config) -> success(processAll(data)))
          models.next = if data.meta.next then next else false
          previous = (success) -> 
            $http({ method: 'GET', url: data.meta.previous })
              .error(report())
              .success((data, status, headers, config) -> success(processAll(data)))
          models.previous = if data.meta.previous then previous else false

          models.total_count = data.meta.total_count
        
        return models
      
      # Public methods

      Model = (data) -> 
        if !data
          data = {}
          Model._loadFromSchema(this)
        angular.extend(this, {_saved:data}, data)

      Model._loadFromSchema = (model) ->
        $http({method: 'GET', url: Model.api_root + 'schema/', cache: true})
          .error(report)
          .success((data, status, headers, config) -> 
            model._saved = {}
            model._required = []
            angular.forEach(data.fields, (info, field) ->
              # Let op! resource_uri is nu ook undefined!
              model._saved[field] = undefined
              if !info.readonly
                if info.default != "No default provided."
                  model[field] = model._saved[field] = info.default
              
                if info.nullable == info.blank == false
                  model._required.push(field)
            )
          )

      Model.api_root = api_root

      Model._more = (data, success) ->
        $http(data)
          .error(report)
          .success((data, status, headers, config) -> success(processAll(data), status, headers, config))

      Model._one = (data, success) ->
        $http(data)
          .error(report)
          .success((data, status, headers, config) -> success(process(data), status, headers, config))
      
      Model.get = (id, success) -> Model._one({method: 'GET', url: Model.api_root + id + '/'}, success)

      Model.all = (success, data) -> 
        data = angular.extend({ method: 'GET', url: Model.api_root , params: {'limit': 10} }, data)
        Model._more(data, success)

      Model.search = (query, success, mod, id) -> 
        if !mod
          mod = 'default'
        Model._more({ method: 'GET', url: Model.api_root + 'search/', params: {'q': query, 'mod': mod, 'searchID': id} }, success)

      Model.getSubresource = (url, success) ->
        if url
          Model._one({method: 'GET', url: url}, success)
        else
          success(null)

      # Instance methods

      Model.prototype.create = (success, error) ->
        model = this
        $http({ method: 'POST', url: Model.api_root , data: this })
          .error(report(error))
          .success((data, status, headers, config) -> 
            data = process(data)
            angular.extend(model, data)
            model._saved = data
            if success
              success(model)
            )

      Model.prototype.update = (success, error) ->
        model = this
        $http({ method: 'PUT', url: model.resource_uri , data: this })
          .error(report(error))
          .success((data, status, headers, config) -> 
            data = process(data)
            angular.extend(model, data)
            model._saved = data
            if success
              success(model)
          )

      Model.prototype.remove = (success, error) ->
        model = this
        $http({ method: 'DELETE', url: model.resource_uri})
          .error(report(error))
          .success((data, status, headers, config) ->
            if success
              success()
          )

      Model.prototype.changed = () ->
        obj = this
        changed = false
        angular.forEach(Object.keys(obj._saved), (key) ->
          if obj[key] != obj._saved[key]
            changed = true
        )
        return changed

      Model.prototype.verify = () ->
        errors = []
        angular.forEach(this._required, (field)->
          if !this[field]
            errors.push(field)
        )
        errors

      Model.prototype.save = (success, error) ->
        if this._delete
          if this.resource_uri
            this.remove(success, error)
        else if this.changed()
          errors = this.verify()
          if errors.length > 0
            if error
              error("REQUIRED_FIELDS_EMPTY: " + errors.join(", "), error)
          else
            if this.resource_uri
              this.update(success, error)
            else
              this.create(success, error)

      return Model
    return Tastypie
  ])
  .value('$strap.config', {
    datepicker: {
      format: 'yyyy-mm-dd'
    }
  })
  .filter('tastypiedate', () ->
    (input) ->
      if input
        parts = input.match(/\d+/g)
        return new Date(parts[0], parts[1] - 1, parts[2], parts[3], parts[4], parts[5])
      else
        return input
  )
  

angular.module('typeahead', [])
  .directive('chSelector', ['$parse', ($parse) ->
    return {
      restrict: 'A',
      require: '?ngModel',
    
      link: (scope, element, attrs, controller) -> 
        ModelGetter = $parse(attrs.ngModel + "_model")
        ModelSetter = ModelGetter.assign

        ModelListgetter = $parse(attrs.chSelector)
        values = ModelListgetter(scope)

        scope.$watch(attrs.chSelector, (newValue, oldValue) -> 
          if newValue != oldValue
            values = newValue
        )

        element.attr('data-provide', 'typeahead')

        setModel = (item) ->
          ModelSetter(scope, item)
          scope.$digest()

        element.typeahead({
          source: (query) -> if angular.isFunction(values) then values.apply(null, arguments) else values
          items: attrs.items || 10
          minLength: attrs.minLength || 1
          matcher: (item) -> true
          sorter: (items) -> items
          updater: (item) -> 
            setModel(item)
            element.one('focus', (event) -> 
              #setModel(undefined)
              #element.val('')
            )
            item.toString()
          highlighter: (item) ->
            query = this.query.replace(/[\-\[\]{}()*+?.,\\\^$|#\s]/g, '\\$&')
            item.toString().replace(new RegExp('(' + query + ')', 'ig'), ($1, match) ->
              '<strong>' + match + '</strong>'
            )
        })

        typeahead = element.data('typeahead');
        typeahead.select = () -> 
          model = this.$menu.find('.active').data('typeahead-model')
          this.$element
            .val(this.updater(model))
            .change()
          this.hide()

        typeahead.render = (items) ->
          that = this

          items = $(items).map((i, item) ->
            i = $(that.options.item).data('typeahead-model', item)
            i.find('a').html(that.highlighter(item))
            return i[0]
          )

          items.first().addClass('active')
          this.$menu.html(items)
          return this

        controller.$formatters.push((obj) -> if obj then obj.toString() else '' )
      }
  ])

angular.module("ngLocale", [], ["$provide", ($provide) ->
  PLURAL_CATEGORY = {ZERO: "zero", ONE: "one", TWO: "two", FEW: "few", MANY: "many", OTHER: "other"}
  $provide.value(
    "$locale"
    {
      "DATETIME_FORMATS": {
        "MONTH":["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"],
        "SHORTMONTH":["jan.","feb.","mrt.","apr.","mei","jun.","jul.","aug.","sep.","okt.","nov.","dec."],
        "DAY":["zondag","maandag","dinsdag","woensdag","donderdag","vrijdag","zaterdag"],
        "SHORTDAY":["zo","ma","di","wo","do","vr","za"],
        "AMPMS":["AM","PM"],
        "medium":"d MMM y HH:mm:ss",
        "short":"dd-MM-yy HH:mm",
        "fullDate":"EEEE d MMMM y",
        "longDate":"d MMMM y",
        "mediumDate":"d MMM y",
        "shortDate":"dd-MM-yy",
        "mediumTime":"HH:mm:ss",
        "shortTime":"HH:mm"
      },
      "NUMBER_FORMATS":{
        "DECIMAL_SEP":",",
        "GROUP_SEP":".",
        "PATTERNS":[{
          "minInt":1,
          "minFrac":0,
          "macFrac":0,
          "posPre":"",
          "posSuf":"",
          "negPre":"-",
          "negSuf":"",
          "gSize":3,
          "lgSize":3,
          "maxFrac":3
          },{
          "minInt":1,
          "minFrac":2,
          "macFrac":0,
          "posPre":"\u00A4 ",
          "posSuf":"",
          "negPre":"\u00A4 -",
          "negSuf":"",
          "gSize":3,
          "lgSize":3,
          "maxFrac":2
          }
        ],
        "CURRENCY_SYM":"€"
      },
      "pluralCat": (n) ->
        if n == 1 
          return PLURAL_CATEGORY.ONE
        return PLURAL_CATEGORY.OTHER
      "id":"nl"
    }
  )
])
