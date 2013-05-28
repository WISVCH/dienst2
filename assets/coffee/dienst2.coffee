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
        $http({method: 'GET', url: Model.api_root + 'schema/'})
          .error(report)
          .success((data, status, headers, config) -> 
            model._saved = {}
            angular.forEach(data.fields, (info, field) ->
              # Let op! resource_uri is nu ook undefined!
              model._saved[field] = undefined
            )
          )

      Model.prototype.changed = () ->
        obj = this
        changed = false
        angular.forEach(Object.keys(obj._saved), (key) ->
          if obj[key] != obj._saved[key]
            changed = true
        )
        return changed

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

      Model.all = (success) -> Model._more({ method: 'GET', url: Model.api_root , params: {'limit': 10} }, success)

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

      return Model
    return Tastypie
  ])
  .value('$strap.config', {
    datepicker: {
      format: 'yyyy-mm-dd'
    }
  });
  

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