"""SJTUsoso URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
"""
from blog.views import *
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from haystack.views import SearchView

from soso.views import *
from django.conf.urls import url
from django.views import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tohome, name='home'),
    path('403/', to403),
    path('404/', to404),
    path('500/', to500),
    path('503/', to503),
    path('category/', tocategory),
    path('contact/', tocontact),
    path('sendmail/', contactme),
    path('forgot/', forgot),
    path('login/', login , name="login"),
    path('page/', topage),
    path("score/<int:Video_id>/", score, name="score"),  # 评分
    path('video/<int:Video_id>/', tovideo,name="Video"),
    path('register/', register),
    path('reset/', reset),
    path('single/<int:Wechat_id>/', tosingle ,name="Wechat"),
    path('search/', mySearchView.as_view(), name='haystack_search'),
    path('search/autocomplete/', autocomplete),
    path('contactsuccess/', contactsuccess),
    path('contactfail/', contactfail),
    path('logout/', logout),

    path("message_boards/<int:fap_id>/<int:pagenum>/", message_boards, name="message_boards"),  # 获取论坛
    path("get_message_board/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", get_message_board,
         name="get_message_board"),  # 获取论坛详情
    path("new_board_comment/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", new_board_comment,
         name="new_board_comment"),  # 发表论坛评论
    path("new_message_board/", new_message_board, name="new_message_board"),  # 发表论坛
    path("like_collect/", like_collect, name="like_collect"),  # 对论坛留言点赞或收藏

    url(r'^captcha', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')),
    url(r'^css/safari\.css$', RedirectView.as_view(url=r'/static/css/safari.css')),
    re_path(r'mdeditor/', include('mdeditor.urls')),
]

urlpatterns += staticfiles_urlpatterns()
