from django.urls import path
from django.urls import re_path

from post.views import ItemListView, ItemCreateView, ItemWeekArchiveView, AVListView

urlpatterns = [
    path("", ItemListView.as_view(), name="post_index"),
    path("create/", ItemCreateView.as_view(), name="post_create"),
    path("av/", AVListView.as_view(), name="post_av"),
    re_path(
        r"^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$",
        ItemWeekArchiveView.as_view(),
        name="post_archive_week",
    ),
]
