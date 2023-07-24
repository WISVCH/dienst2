from django.urls import include, path
from rest_framework import routers

from ldb import viewsets, export
from ldb.views import (
    PersonDetailView,
    PersonDeleteView,
    OrganizationDetailView,
    OrganizationDeleteView,
    PersonEditView,
    OrganizationEditView,
    ResultsView,
    CommitteeMembershipFilterView,
    IndexView,
)

router = routers.DefaultRouter()
router.register(r"people", viewsets.PersonViewSet)
router.register(r"organizations", viewsets.OrganizationsViewSet)

urlpatterns = [
    path("api/v3/", include(router.urls)),
    path("index/", IndexView.as_view(), name="ldb_index"),
    path("people/search/", ResultsView.as_view(), name="ldb_people_search"),
    path("people/<int:pk>/", PersonDetailView.as_view(), name="ldb_people_detail"),
    path(
        "people/<int:pk>/delete/",
        PersonDeleteView.as_view(),
        name="ldb_people_delete",
    ),
    path("people/<int:pk>/edit/", PersonEditView.as_view()),
    path("people/create/", PersonEditView.as_view(), name="ldb_people_create"),
    path(
        "organizations/<int:pk>/",
        OrganizationDetailView.as_view(),
        name="ldb_organizations_detail",
    ),
    path(
        "organizations/<int:pk>/delete/",
        OrganizationDeleteView.as_view(),
        name="ldb_organizations_delete",
    ),
    path("organizations/<int:pk>/edit/", OrganizationEditView.as_view()),
    path(
        "organizations/create/",
        OrganizationEditView.as_view(),
        name="ldb_organizations_create",
    ),
    path("committees/", CommitteeMembershipFilterView.as_view(), name="ldb_committees"),
    path("export/", export.Export.as_view(), name="ldb_export"),
]
