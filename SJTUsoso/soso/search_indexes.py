# -*- coding:utf-8 -*-
#
# by nyLiao, 2020
# ref: https://django-haystack.readthedocs.io/en/master/tutorial.html#setting-up-the-views

from haystack import indexes
from .models import SosoSitearticle


class SosoSitearticleIndex(indexes.SearchIndex, indexes.Indexable):
   text = indexes.CharField(document=True, use_template=True)

   title = indexes.CharField(model_attr='title')            # web title
   url = indexes.CharField(model_attr='url')                # web url
   content = indexes.CharField(model_attr='text')           # web content
   content_auto = indexes.NgramField(model_attr='title')    # autocomplete index
   date = indexes.DateField(model_attr='date')              # web date
   view = indexes.IntegerField(model_attr='view')           # web views times
   sml = indexes.IntegerField(model_attr='sml')             # content similarity

   def get_model(self):
       return SosoSitearticle

   def index_queryset(self, using=None):
       return self.get_model().objects.all()
