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
    path('forgot/', toforgot),
    path('login/', tologin),
    path('page/', topage),
    path('register/', toregister),
    path('reset/', toreset),
    path('single/', tosingle),
    path('search/', SearchView(), name='haystack_search'),
    url(r'^static/(?P<path>.*)$', static.serve, {'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    url(r'^favicon\.ico$', RedirectView.as_view(url=r'static/images/favicon.ico')),
    url(r'^css/safari\.css$', RedirectView.as_view(url=r'/static/css/safari.css')),
    re_path(r'mdeditor/', include('mdeditor.urls')),
]
