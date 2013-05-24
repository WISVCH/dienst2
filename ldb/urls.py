from django.conf.urls.defaults import *
from tastypie.api import Api
from ldb.api import *

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

urlpatterns = patterns('',
    (r'^api/', include(api.urls)),

    url(r'^$', 'ldb.views.index', name="ldb_index"),
)