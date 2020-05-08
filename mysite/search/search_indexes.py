# -*- coding:utf-8 -*-
#
# by nyLiao, 2020
# ref: https://django-haystack.readthedocs.io/en/master/tutorial.html#setting-up-the-views

from haystack import indexes
from .models import ArticleType


class ArticleTypeIndex(indexes.SearchIndex, indexes.Indexable):
   text = indexes.CharField(document=True, use_template=True)

   # id = indexes.CharField(model_attr='id')
   title = indexes.CharField(model_attr='title')        # web title
   date = indexes.CharField(model_attr='date')          # web date
   url = indexes.CharField(model_attr='url')            # web url
   view = indexes.CharField(model_attr='view')          # web views times
   category = indexes.CharField(model_attr='category')  # web class, tags, etc
   content = indexes.CharField(model_attr='content')    # web content

   def get_model(self):
       return ArticleType

   def index_queryset(self, using=None):
       return self.get_model().objects.filter(is_delete=False)
