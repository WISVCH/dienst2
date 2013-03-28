from tastypie.resources import ModelResource
from tastypie import fields
from kas.models import *
from dienst2 import api_helper
from django.forms import ModelForm
from tastypie.validation import FormValidation

class TransactionForm(ModelForm):
  class Meta:
    model = Transaction

class ClosureForm(ModelForm):
  class Meta:
    model = Closure

class TransactionResource(ModelResource):
  get_search = api_helper.get_search(Transaction)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Transaction.objects.all()
    resource_name = 'transaction'
    validation = FormValidation(form_class=TransactionForm)
    filtering = {
      "date": ('lte', 'lt', 'gte', 'gt'),
    }

  closure = fields.CharField(readonly=True)

  def dehydrate_closure(self, bundle):
    return ClosureResource().get_resource_uri(bundle.obj.closure)

  editable = fields.BooleanField(readonly=True)

  def dehydrate_editable(self, bundle):
    return bundle.obj.editable

  def hydrate_user(self, bundle):
    bundle.data['user'] = bundle.request.user.username
    return bundle

class ClosureResource(ModelResource):
  get_search = api_helper.get_search(Closure)
  prepend_urls = api_helper.prepend_urls()

  cashdifference = fields.DecimalField(readonly=True)

  def dehydrate_cashdifference(self, bundle):
    return bundle.obj.cashdifference

  pindifference = fields.DecimalField(readonly=True)

  def dehydrate_pindifference(self, bundle):
    return bundle.obj.pindifference

  previoustotal = fields.DecimalField(readonly=True)

  def dehydrate_previoustotal(self, bundle):
    return getattr(bundle.obj.previous, 'total', 0)

  previousdate = fields.DateField(readonly=True)

  def dehydrate_previousdate(self, bundle):
    return getattr(bundle.obj.previous, 'date', None) 

  def hydrate_user(self, bundle):
    bundle.data['user'] = bundle.request.user.username
    return bundle

  class Meta(api_helper.BaseMeta):
    queryset = Closure.objects.all()
    resource_name = 'closure'
    validation = FormValidation(form_class=ClosureForm)

    filtering = {
      "finished": ('exact')
    }

  # transactions = fields.ToManyField('kas.api.TransactionResource', attribute=lambda bundle: bundle.obj.transactions, readonly=True)