from tastypie.resources import ModelResource
from tastypie import fields
from ldb.models import *
from dienst2 import api_helper
import simplejson

class OrganizationResource(ModelResource):
  get_search = api_helper.get_search(Organization)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Organization.objects.all()
    resource_name = 'organization'

class PersonResource(ModelResource):
  get_search = api_helper.get_search(Person)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Person.objects.all()
    resource_name = 'person'
    filtering = {
      "netid": ('exact'),
      "ldap_username": ('exact')
    }

  member = fields.ToOneField('ldb.api.MemberResource', 'member', null=True)
  student = fields.ToOneField('ldb.api.StudentResource', 'student', null=True)
  alumnus = fields.ToOneField('ldb.api.AlumnusResource', 'alumnus', null=True)
  employee = fields.ToOneField('ldb.api.EmployeeResource', 'employee', null=True)
  living_with = fields.ToOneField('self', 'living_with', null=True)

  age = fields.IntegerField(readonly=True)

  def dehydrate_age(self, bundle):
    try:
      return bundle.obj.age
    except:
      return None

  committees = fields.ToManyField('ldb.api.CommitteeMembershipResource', attribute=lambda bundle: CommitteeMembership.objects.filter(person=bundle.obj), null=True)

class MemberResource(ModelResource):
  get_search = api_helper.get_search(Member)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Member.objects.all()
    resource_name = 'member'

  person = fields.ToOneField('ldb.api.PersonResource', 'person')

class StudentResource(ModelResource):
  get_search = api_helper.get_search(Student)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Student.objects.all()
    resource_name = 'student'

  person = fields.ToOneField('ldb.api.PersonResource', 'person')

class AlumnusResource(ModelResource):
  get_search = api_helper.get_search(Alumnus)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Alumnus.objects.all()
    resource_name = 'alumnus'

  person = fields.ToOneField('ldb.api.PersonResource', 'person')

class EmployeeResource(ModelResource):
  get_search = api_helper.get_search(Employee)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Employee.objects.all()
    resource_name = 'employee'

  person = fields.ToOneField('ldb.api.PersonResource', 'person')

class CommitteeResource(ModelResource):
  get_search = api_helper.get_search(Committee)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = Committee.objects.all()
    resource_name = 'committee'

class CommitteeMembershipResource(ModelResource):
  get_search = api_helper.get_search(CommitteeMembership)
  prepend_urls = api_helper.prepend_urls()

  class Meta(api_helper.BaseMeta):
    queryset = CommitteeMembership.objects.all()
    resource_name = 'committeeMembership'

  person = fields.ToOneField('ldb.api.PersonResource', 'person')
  committee = fields.ToOneField('ldb.api.CommitteeResource', 'committee')
  committeename = fields.CharField(attribute='committee__name')

class ModificationResource(ModelResource):
  class Meta(api_helper.BaseMeta):
    queryset = Modification.objects.all()
    resource_name = 'modification'

  modification = fields.DictField()

  person = fields.ToOneField('ldb.api.PersonResource', 'person')

  def dehydrate_modification(self, bundle):
    return simplejson.loads(bundle.obj.modification)

  def hydrate_modification(self, bundle):
    bundle.obj.modification = simplejson.dumps(bundle.data['modification'])
    return bundle
