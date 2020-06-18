from django.contrib import admin

# Register your models here.
from .models import *

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img_url', 'created_time', 'last_updated_time','create_month')

@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')

@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'nickname', 'password', 'email', 'sex')

@admin.register(Collection)
class UserAdmin(admin.ModelAdmin):
    list_display = ('user', 'itemtype', 'itemtitle', 'itempk')