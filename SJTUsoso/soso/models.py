from django.db import models

# Create your models here.
import os
import time
import calendar
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField
from mdeditor.fields import MDTextField


# Create your models here.
class SosoSitearticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    date = models.DateField()                   # web date
    view = models.IntegerField()                # web views times
    category = models.CharField(max_length=20, blank=True, null=True)
    kw1 = models.CharField(max_length=20, blank=True, null=True)
    kw2 = models.CharField(max_length=20, blank=True, null=True)
    kw3 = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'soso_siteArticle'
