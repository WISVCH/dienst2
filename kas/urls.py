from django.conf.urls import patterns, include, url
from tastypie.api import Api

from kas.api import *


api = Api(api_name='v2')
api.register(TransactionResource())
api.register(ClosureResource())

urlpatterns = patterns('',
                       (r'^api/', include(api.urls)),

                       url(r'^$', 'kas.views.index', name="kas_index"),
)
