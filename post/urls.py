from __future__ import unicode_literals

from django.urls import re_path

from post.views import ItemListView, ItemCreateView, ItemWeekArchiveView, AVListView

urlpatterns = [
    re_path(r"^$", ItemListView.as_view(), name="post_index"),
    re_path(r"^create/$", ItemCreateView.as_view(), name="post_create"),
    re_path(r"^av/$", AVListView.as_view(), name="post_av"),
    re_path(
        r"^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$",
        ItemWeekArchiveView.as_view(),
        name="post_archive_week",
    ),
]
