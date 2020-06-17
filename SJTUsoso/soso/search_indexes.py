# -*- coding:utf-8 -*-
#
# by nyLiao, 2020
# ref: https://django-haystack.readthedocs.io/en/master/tutorial.html#setting-up-the-views

from haystack import indexes
from .models import SosoSitearticle


class SosoSitearticleIndex(indexes.SearchIndex, indexes.Indexable):
   text = indexes.CharField(document=True, use_template=True)

   title = indexes.CharField(model_attr='title')        # web title
   url = indexes.CharField(model_attr='url')            # web url
   content = indexes.CharField(model_attr='text')    # web content

   def get_model(self):
       return SosoSitearticle

   def index_queryset(self, using=None):
       return self.get_model().objects.all()
