from __future__ import unicode_literals

from django.conf.urls import url

from post.views import ItemListView, ItemCreateView, ItemWeekArchiveView, AVListView

urlpatterns = [
    url(r'^$', ItemListView.as_view(), name='post_index'),
    url(r'^create/$', ItemCreateView.as_view(), name='post_create'),
    url(r'^av/$', AVListView.as_view(), name='post_av'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$',
        ItemWeekArchiveView.as_view(),
        name="post_archive_week"),
]
