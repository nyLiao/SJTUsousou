from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User as superUser
import time
import calendar
import random
from django.conf import settings
import os
from mdeditor.fields import MDTextField
from django.db import models
from django.db.models import Avg
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class User(models.Model):
    '''用户表'''
    gender = (
        ('male','男'),
        ('female','女'),
    )
    img_url = models.ImageField(upload_to='images', blank=True)
    name = models.CharField(max_length=128,unique=True)
    nickname = models.CharField(max_length=128,default='Freshman')
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32,choices=gender,default='男')
    c_time = models.DateTimeField(auto_now_add=True)

    def getImage(self):
        if self.img_url:
            return self.img_url.url
        else:
            return os.path.join("/media/images", "avatar-" + str(random.randint(1, 8)) + ".jpg")

    def __str__(self):
        return self.name
    class Meta:
        ordering = ['c_time']
        verbose_name = 'user'
        verbose_name_plural = 'user'

class MessageBoard(models.Model):
    # 读书论坛
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    title = models.CharField(max_length=64, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    look_num = models.IntegerField(verbose_name='点击数', default=1)
    like_num = models.IntegerField(verbose_name='点赞数', default=0)
    feebback_num = models.IntegerField(verbose_name='回复数', default=0)
    collect_num = models.IntegerField(verbose_name='收藏数', default=0)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "留言"
        verbose_name_plural = verbose_name


class CollectBoard(models.Model):
    # 收藏、点赞留言帖子
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="留言")
    create_time = models.DateTimeField(auto_now_add=True)
    is_collect = models.BooleanField(default=False, verbose_name='是否收藏')
    is_like = models.BooleanField(default=False, verbose_name='是否点赞')

    class Meta:
        verbose_name = "收藏/点赞留言"
        verbose_name_plural = verbose_name


class BoardComment(models.Model):
    # 回复留言
    message_board = models.ForeignKey(MessageBoard, on_delete=models.CASCADE, verbose_name="留言")
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="用户", related_name="user"
    )
    content = models.TextField( verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "子留言"
        verbose_name_plural = verbose_name

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

class Blog(models.Model,ReadNumExpandMethod,LikeNumExpandMethod):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING,default=None)
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING,default=None)
    content = RichTextUploadingField()
    created_time = models.DateTimeField(auto_now_add=False)
    last_updated_time = models.DateTimeField(auto_now=True)
    create_month = models.CharField(max_length=50,blank=False,default=calendar.month_name[int(time.localtime().tm_mon)])
    img_url = models.ImageField(upload_to='images',blank=True)  # upload_to指定图片上传的途径，如果不存在则自动创建
    def __str__(self):
        return "<Blog: %s>" % self.title
    def getImage(self):
        if self.img_url:
            return self.img_url.url
        else:
            return os.path.join("/media/images","project-"+str(random.randint(1,8))+".jpg")
    class Meta:
        ordering = ['-created_time']

class Wechat(models.Model):
    title = models.CharField(verbose_name="标题", max_length=300)
    digest = models.CharField(verbose_name="摘要", max_length=300)
    tag = models.CharField(verbose_name="标签", max_length=20)
    img = models.CharField(verbose_name="图片", max_length=300)
    date = models.CharField(verbose_name="日期", max_length=100)
    content = models.CharField(verbose_name="内容", max_length=2000)
    objects = models.Manager()
    class Meta:
        verbose_name = "公众号"
        verbose_name_plural = "公众号"

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(verbose_name="标题", max_length=100)
    tag = models.CharField(verbose_name="标签", max_length=50)
    video = models.CharField(verbose_name="视频", max_length=100)
    date = models.CharField(verbose_name="日期", max_length=50)
    preload = models.CharField(verbose_name="封面", max_length=50)
    love = models.IntegerField(default=0, blank=True)
    collect = models.IntegerField(default=0, blank=True)
    watch = models.IntegerField(default=0, blank=True)
    rate_num = models.IntegerField(default=0, blank=True)
    avg = models.FloatField(default=0,verbose_name="均分")

    objects = models.Manager()
    class Meta:
        verbose_name = "视频"
        verbose_name_plural = "视频"

    def __str__(self):
        return self.title

class VideoComments(models.Model):
    content = models.CharField(verbose_name="内容", max_length=300)
    date = models.CharField(verbose_name="日期", max_length=50)
    user_nickname = models.CharField(verbose_name="昵称", max_length=50)
    user_id = models.IntegerField(default=0, blank=True)
    video_id = models.IntegerField(default=0, blank=True)
    objects = models.Manager()
    class Meta:
        verbose_name = "视频评论"
        verbose_name_plural = "视频评论"

class Rate(models.Model):
    video = models.ForeignKey(
        Video, on_delete=models.CASCADE, blank=True, null=True, verbose_name="图书id"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, verbose_name="用户id",
    )
    mark = models.FloatField(verbose_name="评分")
    create_time = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)

    @property
    def avg_mark(self):
        average = Rate.objects.all().aggregate(Avg('mark'))['mark__avg']
        return average

    class Meta:
        verbose_name = "评分信息"
        verbose_name_plural = verbose_name