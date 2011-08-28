import datetime
from haystack.indexes import *
from haystack import site
from ldb.models import *

class PersonIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    username = CharField(model_attr='ldap_username')
    # pub_date = DateTimeField(model_attr='pub_date')
site.register(Person, PersonIndex)

class OrganizationIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
site.register(Organization, OrganizationIndex)