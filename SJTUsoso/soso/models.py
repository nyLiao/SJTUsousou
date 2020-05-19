from django.db import models

# Create your models here.
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import time
import calendar
import random
from django.conf import settings
import os
from mdeditor.fields import MDTextField


from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0



class LikeNum(models.Model):
    like_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType, on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class LikeNumExpandMethod():
    def get_like_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            likenum = LikeNum.objects.get(content_type=ct, object_id=self.pk)
            return likenum.like_num
        except exceptions.ObjectDoesNotExist:
            return 0


class BlogType(models.Model):
    type_name = models.CharField(max_length=50)

    def __str__(self):
        return self.type_name
'''
class siteArticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)        # web title
    date = models.DateField()                       # web date
    url = models.CharField(max_length=128)          # web url
    view = models.IntegerField()                    # web views times
    category = models.CharField(max_length=128)     # web class, tags, etc
    content = models.TextField()                    # web content
    is_delete = models.BooleanField(default=False)
'''
class SosoSitearticle(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'soso_siteArticle'
