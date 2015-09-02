from haystack import indexes

from ldb.models import Person, Organization


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(use_template=True, boost=1.1)
    address = indexes.CharField(use_template=True, boost=.9)
    contact = indexes.CharField(use_template=True, boost=.95)
    ldap_username = indexes.CharField(model_attr="ldap_username", boost=1.1)

    def get_model(self):
        return Person


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(use_template=True, boost=1.5)
    address = indexes.CharField(use_template=True, boost=.5)
    contact = indexes.CharField(use_template=True, boost=.85)

    def get_model(self):
        return Organization
