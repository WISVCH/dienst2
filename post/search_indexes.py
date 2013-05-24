import datetime
from haystack import indexes
from post.models import Category, Source, Item

class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)

  def get_model(self):
    return Category

class SourceIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)

  def get_model(self):
    return Source

class ItemIndex(indexes.SearchIndex, indexes.Indexable):
  text = indexes.CharField(document=True, use_template=True)

  def get_model(self):
    return Item
