import datetime
from haystack import indexes
from ldb.models import Person, Organization

class PersonIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)

  def get_model(self):
    return Person

class OrganizationIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)

  def get_model(self):
    return Organization