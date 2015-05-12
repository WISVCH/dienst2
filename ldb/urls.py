from django.conf.urls import patterns, include, url
from tastypie.api import Api
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

urlpatterns = patterns('',
    (r'^api/', include(api.urls)),

    url(r'^$', 'ldb.views.index', name="ldb_index"),
)
