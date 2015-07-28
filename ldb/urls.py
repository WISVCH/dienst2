from django.conf.urls import patterns, include, url
from rest_framework import routers
from tastypie.api import Api

from ldb import views_api
from ldb.api import *
from ldb.export import ExportResource
from ldb.views import PersonDetailView, PersonDeleteView, OrganizationDetailView, OrganizationDeleteView, \
    organization_edit, ajax_people_search, index_old, PersonEditView

api = Api(api_name='v2')

api.register(OrganizationResource())
api.register(PersonResource())
api.register(MemberResource())
api.register(StudentResource())
api.register(AlumnusResource())
api.register(EmployeeResource())
api.register(CommitteeResource())
api.register(CommitteeMembershipResource())
api.register(ModificationResource())
api.register(ExportResource())

router = routers.DefaultRouter()
router.register(r'people', views_api.PersonViewSet)
router.register(r'organizations', views_api.OrganizationsViewSet)

urlpatterns = patterns(
    '',
    (r'^api/', include(api.urls)),

    url(r'^$', 'ldb.views.index', name="ldb_index"),

    url(r'^api/v3/', include(router.urls)),
    # url(r'^api/v3/api-auth/', include('rest_framework.urls', namespace='rest_framework'))

    url(r'^old/$', index_old, name='ldb_index_old'),

    url(r'^people/search/$', ajax_people_search, name='ldb_people_search' ),

    url(r'^people/(?P<pk>\d+)/$', PersonDetailView.as_view(), name='ldb_people_detail'),
    url(r'^people/(?P<pk>\d+)/delete/$', PersonDeleteView.as_view(), name='ldb_people_delete'),
    url(r'^people/(?P<pk>\d+)/edit/$', PersonEditView.as_view()),
    url(r'^people/create/$', PersonEditView.as_view(), name='ldb_people_create'),

    url(r'^organizations/(?P<pk>\d+)/$', OrganizationDetailView.as_view(),
        name='ldb_organizations_detail'),
    url(r'^organizations/(?P<pk>\d+)/delete/$', OrganizationDeleteView.as_view(),
        name='ldb_organizations_delete'),
    url(r'^organizations/(?P<pk>\d+)/edit/$', organization_edit),
    url(r'^organizations/create/$', organization_edit, name='ldb_organizations_create'),

)
