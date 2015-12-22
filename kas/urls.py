from django.conf.urls import patterns, include, url
from tastypie.api import Api

from kas.api import *
from kas.views import KasIndex, TransactionsView

api = Api(api_name='v2')
api.register(TransactionResource())
api.register(ClosureResource())

urlpatterns = patterns(
    '',
    (r'^api/', include(api.urls)),

    url(r'^$', 'kas.views.index', name="kas_index_angular"),

    url(r'^index/$', KasIndex.as_view(), name='kas_index'),

    url(r'^transactions/search/$', TransactionsView.as_view(), name='kas_transaction_search')
)
