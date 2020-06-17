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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.views import static
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from haystack.views import SearchView

from soso.views import *
from myadmin.views import *
from blog.views import *

urlpatterns = [
    path('myadmin/', tomain,name="myadmin"),
    path('video_resource/', tovideo_resource,name="video_resource"),
    path('wechat_resource/', towechat_resource,name="wechat_resource"),
    path('del_video_resource/<int:Video_id>/', to_del_video,name="del_video_resource"),
    path('del_wechat_resource/<int:Wechat_id>/', to_del_wechat,name="del_wechat_resource"),
    path('upload/', upload_resource,name="upload"),
    path('check/', check_comment,name="check"),
    path('count/', count_resource,name="count"),
    path('post1/',video_post,name="post1"),
    path('post2/',wechat_post,name="post2"),
    path('cluster/',user_cluster,name="cluster"),
    path('video_comment/<int:Video_id>/',comment_push,name="video_comment"),

    path('admin/', admin.site.urls),
    path('', tohome, name='home'),
    path('403/', to403),
    path('404/', to404),
    path('500/', to500),
    path('503/', to503),

    path('page/', topage),

    path("score/<int:Video_id>/", score, name="score"),  # 评分
    path('video/<int:Video_id>/', tovideo,name="Video"),

    path('register/', register),
    path('login/', login, name="login"),
    path('logout/', logout),
    path('forgot/', forgot),
    path('reset/', reset),

    path('single/<int:Wechat_id>/', tosingle ,name="Wechat"),
    path('search/', mySearchView.as_view(), name='haystack_search'),
    path('search/autocomplete/', autocomplete),

    path('userspace/', userspace),
    path('userspace/change/', userspacechange),
    path('userspace/avatar/', avatarup),

    path('blog/write/', WBlog),
    path('blog/delete/', deblog),
    path('blog/', blog_list, name="blog_list"),
    path('blog/coverup/', coverup),
    path('blog/<int:blog_pk>/', blog_detail, name="blog_detail"),

    path('collect/', collect),
    path('decollect/', decollect),

    path('contact/', contactme),
    path('contactsuccess/', contactsuccess),
    path('contactfail/', contactfail),

    path("message_boards/<int:fap_id>/<int:pagenum>/", message_boards, name="message_boards"),  # 获取论坛
    path("get_message_board/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", get_message_board,
         name="get_message_board"),  # 获取论坛详情
    path("new_board_comment/<int:message_board_id>/<int:fap_id>/<int:currentpage>/", new_board_comment,
         name="new_board_comment"),  # 发表论坛评论
    path("new_message_board/", new_message_board, name="new_message_board"),  # 发表论坛
    path("like_collect/", like_collect, name="like_collect"),  # 对论坛留言点赞或收藏

    url(r'^captcha', include('captcha.urls')),
    url(r'^blog/write/ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')),
    url(r'^css/safari\.css$', RedirectView.as_view(url=r'/static/css/safari.css')),
]

urlpatterns += staticfiles_urlpatterns()
