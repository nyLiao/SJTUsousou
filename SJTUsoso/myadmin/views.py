from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Video
from blog.models import Wechat
from blog.models import User
from blog.models import Rate
from blog.models import VideoComments
from blog.renew_tfidf import tfidf,cal
from django.shortcuts import HttpResponse
from .cluster import *
import datetime
def tomain(request):
    return render(request, "user/welcome.html", {"title": "欢迎来到管理员界面"})

def videos_paginator(videos, page):
    paginator = Paginator(videos, 6)
    if page is None:
        page = 1
    videos = paginator.page(page)
    return videos

def tovideo_resource(request):
    videos = Video.objects.all()
    paginator = Paginator(videos, 5)
    current_page = request.GET.get("page", 1)
    videos = paginator.page(current_page)
    return render(request, "user/item.html", {"videos": videos, "title": "视频资源"})

def towechat_resource(request):
    wechats = Wechat.objects.all()
    paginator = Paginator(wechats, 5)
    current_page = request.GET.get("page", 1)
    wechats = paginator.page(current_page)
    return render(request, "user/items2.html", {"wechats": wechats, "title": "公众号资源"})

def to_del_video(request,Video_id):
    Video.objects.get(id=Video_id).delete()
    videos = Video.objects.all()
    paginator = Paginator(videos, 5)
    current_page = request.GET.get("page", 1)
    videos = paginator.page(current_page)
    return render(request, "user/item.html", {"videos": videos, "title": "视频资源"})

def to_del_wechat(request,Wechat_id):
    Wechat.objects.get(id=Wechat_id).delete()
    wechats = Wechat.objects.all()
    paginator = Paginator(wechats, 5)
    current_page = request.GET.get("page", 1)
    wechats = paginator.page(current_page)
    tfidf()
    return render(request, "user/items2.html", {"wechats": wechats, "title": "公众号资源"})

def upload_resource(request):
    return render(request, "user/upload.html", {"title": "上传资源"})

def count_resource(request):
    user_num = User.objects.all().count()
    video_num = Video.objects.all().count()
    wechat_num = Wechat.objects.all().count()
    rate_num = Rate.objects.all().count()
    return render(request, "user/resource_count.html", locals())

def video_post(request):
    if request.method == 'POST':
        myFile = request.FILES.get("video", None)
        destination = open("D:\\venv\\SJTUsousou\\SJTUsoso\\static\\images\\videos\\" + myFile.name, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        myFile1 = request.FILES.get("preload", None)
        destination = open("D:\\venv\\SJTUsousou\\SJTUsoso\\static\\images\\preload\\" + myFile1.name, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile1.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        title=request.POST.get('title','')
        tag=request.POST.get('tag','')
        now_time = datetime.datetime.now()
        obj = Video(date=now_time,title=title, tag=tag , video=myFile.name,preload=myFile1.name,love=0,watch=0,collect=0,avg=0,rate_num=0,)
        obj.save()

        return HttpResponse("视频上传成功")
    else:
        return HttpResponse("程序错误，请回退重试")

def wechat_post(request):
    if request.method == 'POST':
        myFile = request.FILES.get("pic", None)
        destination = open("D:\\venv\\SJTUsousou\\SJTUsoso\\static\\images\\wechat\\" + myFile.name,
                           'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        title = request.POST.get('title', '')
        tag = request.POST.get('tag', '')
        digest = request.POST.get('digest', '')
        content = request.POST.get('content', '')
        now_time = datetime.datetime.now()
        obj = Wechat(date=now_time, title=title, tag=tag, img=myFile.name, digest=digest,content=content)
        obj.save()
        tfidf()
        return HttpResponse("公众号文章上传成功")
    else:
        return HttpResponse("程序错误，请回退重试")

def user_cluster(request):
    users= kmeans_cluster ()
    tag =  list(Video.objects.values_list("tag"))
    return render(request, "user/cluster.html", {"title": "欢迎来到用户聚类界面","users": users,"tag": tag})

def comment_push(request,Video_id):
    if request.method == 'POST':
        content = request.POST.get('content', '')
        now_time = datetime.datetime.now()
        user = User.objects.get(id=request.session.get("user_id"))
        obj = VideoComments(date=now_time, user_id=user.id,video_id=Video_id,content=content,user_nickname=user.nickname)
        obj.save()
        return HttpResponse("评论上传成功")
    else:
        return HttpResponse("程序错误，请回退重试")

def check_comment(request):
    return render(request, "user/check_comment.html", {"title": "欢迎来到评论监管界面"})
