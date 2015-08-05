from haystack import indexes

from ldb.models import Person, Organization


class PersonIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(use_template=True, boost=1.5)
    address = indexes.CharField(use_template=True, boost=.5)
    contact = indexes.CharField(use_template=True, boost=.85)

    def get_model(self):
        return Person


class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    name = indexes.CharField(use_template=True, boost=1.5)
    address = indexes.CharField(use_template=True, boost=.5)
    contact = indexes.CharField(use_template=True, boost=.85)

    def get_model(self):
        return Organization
