from django.conf.urls import patterns, url, include
from tastypie.api import Api

from post.api import *
from post.views import ItemListView, ItemCreateView, ItemWeekArchiveView, AVListView

api = Api(api_name='v2')
api.register(CategoryResource())
api.register(SourceResource())
api.register(ItemResource())

urlpatterns = patterns('',
                       (r'^api/', include(api.urls)),

                       url(r'^$', 'post.views.index', name="post_index_angular"),

                       url(r'^index/$', ItemListView.as_view(), name='post_index'),
                       url(r'^create/$', ItemCreateView.as_view(), name='post_create'),
                       url(r'^av/$', AVListView.as_view(), name='post_av'),
                       url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
                           ItemWeekArchiveView.as_view(),
                           name="post_archive_week"),
                       )
