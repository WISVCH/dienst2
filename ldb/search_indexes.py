from __future__ import unicode_literals

from haystack import indexes

from ldb.models import Organization, Person


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(use_template=True, boost=1.1)
    address = indexes.CharField(use_template=True, boost=.9)
    contact = indexes.CharField(use_template=True, boost=.95)
    ldap_username = indexes.CharField(model_attr="ldap_username", boost=1.1, null=True)

    def get_model(self):
        return Person


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(use_template=True, boost=1.1)
    address = indexes.CharField(use_template=True, boost=.9)
    contact = indexes.CharField(use_template=True, boost=.95)

    def get_model(self):
        return Organization
