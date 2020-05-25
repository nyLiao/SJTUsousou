from django.db import models

# Create your models here.
from django.db import models
from django.db.models import Avg
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

class MessageBoard (models.Model):
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


class CollectBoard (models.Model):
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