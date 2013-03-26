from tastypie.resources import ModelResource
from tastypie import fields
from kas.models import *
from dienst2 import api_helper

class TransactionResource(ModelResource):
  get_search = api_helper.get_search(Transaction)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Transaction.objects.all()
    resource_name = 'transaction'

  closure = fields.CharField(readonly=True)

  def dehydrate_closure(self, bundle):
    return ClosureResource().get_resource_uri(bundle.obj.closure())

  def hydrate_user(self, bundle):
    bundle.data['user'] = bundle.request.user.username
    return bundle

class ClosureResource(ModelResource):
  get_search = api_helper.get_search(Closure)
  prepend_urls = api_helper.prepend_urls()

  cashdifference = fields.DecimalField(readonly=True)

  def dehydrate_cashdifference(self, bundle):
    return bundle.obj.cashdifference()

  pindifference = fields.DecimalField(readonly=True)

  def dehydrate_pindifference(self, bundle):
    return bundle.obj.pindifference()

  class Meta(api_helper.BaseMeta):
    queryset = Closure.objects.all()
    resource_name = 'closure'

  transactions = fields.ToManyField('kas.api.TransactionResource', attribute=lambda bundle: bundle.obj.transactions(), readonly=True)