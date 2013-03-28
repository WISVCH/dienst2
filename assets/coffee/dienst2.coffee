$ = window.jQuery

report = (data, status, headers, config) ->
  throw { message: 'Server communication failed.', status: status, config: config }

angular.module('dienst2', [])
  .factory('Tastypie', ['$http', ($http) ->
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
              .error(report)
              .success((data, status, headers, config) -> success(processAll(data)))
          models.next = if data.meta.next then next else false
          previous = (success) -> 
            $http({ method: 'GET', url: data.meta.previous })
              .error(report)
              .success((data, status, headers, config) -> success(processAll(data)))
          models.previous = if data.meta.previous then previous else false

          models.total_count = data.meta.total_count
        
        return models
      
      # Public methods

      Model = (data) -> 
        angular.extend(this, data)

      Model.api_root = api_root

      Model._more = (data, success) ->
        $http(data)
          .error(report)
          .success((data, status, headers, config) -> success(processAll(data)))

      Model._one = (data, success) ->
        $http(data)
          .error(report)
          .success((data, status, headers, config) -> success(process(data)))
      
      Model.get = (id, success) -> Model._one({method: 'GET', url: Model.api_root + id + '/'}, success)

      Model.all = (success) -> Model._more({ method: 'GET', url: Model.api_root , params: {'limit': 10} }, success)

      Model.search = (query, success) -> Model._more({ method: 'GET', url: Model.api_root + 'search/', params: {'q': query} }, success)

      Model.getSubresource = (url, success) ->
        Model._one({method: 'GET', url: url}, success)

      # Instance methods

      Model.prototype.create = (success) ->
        $http({ method: 'POST', url: Model.api_root , data: this })
          .error(report)
          .success((data, status, headers, config) -> success(process(data)))

      Model.prototype.update = (success) ->
        model = this
        $http({ method: 'PUT', url: Model.api_root + this.id + '/' , data: this })
          .error(report)
          .success((data, status, headers, config) -> 
            angular.extend(model, process(data))
            if success
              success(model)
          )

      return Model
    return Tastypie
  ])
  

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
              setModel(undefined)
              element.val('')
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
      }
  ])