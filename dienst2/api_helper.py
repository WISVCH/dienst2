from django.conf.urls.defaults import *
from django.core.paginator import Paginator, InvalidPage
from django.http import Http404
from haystack.query import SearchQuerySet
from haystack.inputs import Raw
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.utils import trailing_slash
from tastypie.cache import SimpleCache
from tastypie.validation import Validation
from django.core.exceptions import ValidationError

class CHValidation(Validation):
  def is_valid(self, bundle, request=None):
    try:
      bundle.obj.full_clean()
    except ValidationError as e:
      return e

    return {}

def prepend_urls():
  def prepend_urls(self):
    return [
      url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_search_" + self._meta.resource_name),
    ]
  return prepend_urls

def get_search(Model):
  def get_search(self, request, **kwargs):
    self.method_check(request, allowed=['get'])
    self.is_authenticated(request)
    self.throttle_check(request)

    # Do the query.
    sqs = SearchQuerySet().models(Model)
    
    words = request.GET.get('q', '').split(' ')
    mod = request.GET.get('mod', 'default')
    for word in words:
      
      if mod == 'default':
        word = '*' + word + '*'
      elif mod == 'start':
        word = word + '*'
      elif mod == 'exact':
        word = word

      sqs = sqs.filter(text=Raw(word))
    sqs = sqs.load_all()

    paginator = Paginator(sqs, 20)

    try:
      page = paginator.page(int(request.GET.get('page', 1)))
    except InvalidPage:
      raise Http404("Sorry, no results on that page.")

    objects = []

    for result in page.object_list:
      bundle = self.build_bundle(obj=result.object, request=request)
      bundle = self.full_dehydrate(bundle)
      objects.append(bundle)

    object_list = {
      'objects': objects,
      'meta': {'total_count': len(sqs)}
    }

    self.log_throttled_access(request)
    return self.create_response(request, object_list)
  return get_search

class BaseMeta:
  authorization= DjangoAuthorization()
  always_return_data = True
  cache = SimpleCache(timeout=10)
  validation = CHValidation()
