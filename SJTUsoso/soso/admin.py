from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(SosoSitearticle)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'url', 'img_url')