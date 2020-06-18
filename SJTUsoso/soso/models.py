from django.db import models

# Create your models here.
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
import time
import calendar
import random

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions
from ckeditor_uploader.fields import RichTextUploadingField
import os
from mdeditor.fields import MDTextField


from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
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
    img_url = models.ImageField(upload_to='images', blank=True)
    sml = models.IntegerField(blank=True, null=True, default=0)

    def getImage(self):
        if self.img_url:
            return self.img_url.url
        else:
            return os.path.join("/media/images","soso-"+str(random.randint(1,10))+".jpg")

    class Meta:
        #managed = False
        db_table = 'soso_siteArticle'
