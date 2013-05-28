from tastypie.resources import ModelResource
from tastypie.constants import ALL, ALL_WITH_RELATIONS
from tastypie import fields
from post.models import *
from dienst2 import api_helper

from django.db.models import Q

class CategoryResource(ModelResource):
  get_search = api_helper.get_search(Category)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Category.objects.all()
    resource_name = 'category'

class SourceResource(ModelResource):
  get_search = api_helper.get_search(Source)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Source.objects.all()
    resource_name = 'source'

  usage = fields.IntegerField(readonly=True)

  def dehydrate_usage(self, bundle):
    try:
      return Item.objects.filter(
        Q(receiver=bundle.obj) |
        Q(sender=bundle.obj)
      ).count()
    except:
      return 0

class ItemResource(ModelResource):
  get_search = api_helper.get_search(Item)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Item.objects.all()
    resource_name = 'item'
    filtering = {
      "date": ('lte', 'lt', 'gte', 'gt'),
      "category": ('exact')
    }

  category = fields.ToOneField(CategoryResource, 'category')
  sender = fields.ToOneField(SourceResource, 'sender')
  receiver = fields.ToOneField(SourceResource, 'receiver')

  categoryname = fields.CharField(attribute='category__name', readonly=True)
  sendername = fields.CharField(attribute='sender__name', readonly=True)
  receivername = fields.CharField(attribute='receiver__name', readonly=True)