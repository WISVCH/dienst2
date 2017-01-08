from __future__ import unicode_literals

from django.conf.urls import include, url
from rest_framework import routers
from tastypie.api import Api

from ldb import viewsets
from ldb.export import ExportResource
from ldb.views import PersonDetailView, PersonDeleteView, OrganizationDetailView, OrganizationDeleteView, \
    PersonEditView, OrganizationEditView, ResultsView, CommitteeMembershipFilterView, IndexView, AngularIndexView

api = Api(api_name='v2')
api.register(ExportResource())

router = routers.DefaultRouter()
router.register(r'people', viewsets.PersonViewSet)
router.register(r'organizations', viewsets.OrganizationsViewSet)

urlpatterns = [
    url(r'^api/', include(api.urls)),

    url(r'^$', AngularIndexView.as_view(), name="ldb_index_angular"),

    url(r'^api/v3/', include(router.urls)),
    # url(r'^api/v3/api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    url(r'^index/$', IndexView.as_view(), name='ldb_index'),

    url(r'^people/search/$', ResultsView.as_view(), name='ldb_people_search'),

    url(r'^people/(?P<pk>\d+)/$', PersonDetailView.as_view(), name='ldb_people_detail'),
    url(r'^people/(?P<pk>\d+)/delete/$', PersonDeleteView.as_view(), name='ldb_people_delete'),
    url(r'^people/(?P<pk>\d+)/edit/$', PersonEditView.as_view()),
    url(r'^people/create/$', PersonEditView.as_view(), name='ldb_people_create'),

    url(r'^organizations/(?P<pk>\d+)/$', OrganizationDetailView.as_view(),
        name='ldb_organizations_detail'),
    url(r'^organizations/(?P<pk>\d+)/delete/$', OrganizationDeleteView.as_view(),
        name='ldb_organizations_delete'),
    url(r'^organizations/(?P<pk>\d+)/edit/$', OrganizationEditView.as_view()),
    url(r'^organizations/create/$', OrganizationEditView.as_view(), name='ldb_organizations_create'),
    url(r'^committees/$', CommitteeMembershipFilterView.as_view(), name='ldb_committees'),
]
