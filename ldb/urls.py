from django.conf.urls import patterns, include, url
from rest_framework import routers
from tastypie.api import Api

from ldb import views_api
from ldb.api import *
from ldb.export import ExportResource

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

urlpatterns = patterns('',
                       (r'^api/', include(api.urls)),

                       url(r'^$', 'ldb.views.index', name="ldb_index"),

                       url(r'^api/v3/', include(router.urls)),
                       # url(r'^api/v3/api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)
