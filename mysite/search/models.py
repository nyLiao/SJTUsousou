from django.db import models

# Create your models here.

class ArticleType(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=256)        # web title
    date = models.DateField()                       # web date
    url = models.CharField(max_length=128)          # web url
    view = models.IntegerField()                    # web views times
    category = models.CharField(max_length=128)     # web class, tags, etc
    content = models.TextField()                    # web content
    is_delete = models.BooleanField(default=False)
