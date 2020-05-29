# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy_djangoitem import DjangoItem
from soso.models import SosoSitearticle

class ArticleItem(DjangoItem):
    django_model = SosoSitearticle
