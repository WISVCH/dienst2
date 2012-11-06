from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from ldb.models import Person, Entity
from ldb.views import *
from ldb.resources import *
from djangorestframework.resources import ModelResource
from djangorestframework.views import ListOrCreateModelView, InstanceModelView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', index, name='index'),

    url(r'^people/search/$', ajax_people_search, name='ldb_people_search' ),

    url(r'^people/(?P<pk>\d+)/$', PersonDetailView.as_view(), name='ldb_people_detail'),
    url(r'^people/(?P<pk>\d+)/delete/$', PersonDeleteView.as_view(), name='ldb_people_delete'),
    url(r'^people/(?P<pk>\d+)/edit/$', person_edit),
    url(r'^people/create/$', person_edit, name='ldb_people_create'),

    url(r'^organizations/(?P<pk>\d+)/$', OrganizationDetailView.as_view(), name='ldb_organizations_detail'),
    url(r'^organizations/(?P<pk>\d+)/delete/$', OrganizationDeleteView.as_view(), name='ldb_organizations_delete'),
    url(r'^organizations/(?P<pk>\d+)/edit/$', organization_edit),
    url(r'^organizations/create/$', organization_edit, name='ldb_organizations_create'),
    
    url(r'^search/', include('haystack.urls')),

    url(r'^ldb/export/$', export_lists, name='ldb_export_lists'),
    url(r'^ldb/export/(?P<type>\w+)/(?P<list>\w+)/$', export_lists, name="ldb_export_list"),

    url(r'^api/people/$', ListOrCreateModelView.as_view(resource=PersonResource), name='person-resource-root'),
    url(r'^api/people/(?P<pk>\d+)/$', InstanceModelView.as_view(resource=PersonFullResource)),

    url(r'^api/members/$', ListOrCreateModelView.as_view(resource=MemberResource), name='member-resource-root'),
    url(r'^api/members/(?P<pk>\d+)/$', InstanceModelView.as_view(resource=MemberFullResource)),

    url(r'^api/alumni/$', ListOrCreateModelView.as_view(resource=AlumnusResource), name='alumnus-resource-root'),
    url(r'^api/alumni/(?P<pk>\d+)/$', InstanceModelView.as_view(resource=AlumnusFullResource)),
)
