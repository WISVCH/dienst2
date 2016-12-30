from __future__ import unicode_literals

from django.conf.urls import include, url
from tastypie.api import Api

from kas.api import TransactionResource, ClosureResource
from kas.views import index

api = Api(api_name='v2')
api.register(TransactionResource())
api.register(ClosureResource())

urlpatterns = [
    url(r'^api/', include(api.urls)),
    url(r'^$', index, name="kas_index"),
]
