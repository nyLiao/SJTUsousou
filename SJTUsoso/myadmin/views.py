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
import json
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
    comment_num = VideoComments.objects.all().count()
    return render(request, "user/resource_count.html", locals())

def video_post(request):
    if request.method == 'POST':
        myFile = request.FILES.get("video", None)
        destination = open("/root/SJTUsoso/static/images/videos/" + myFile.name, 'wb+')  # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():  # 分块写入文件
            destination.write(chunk)
        destination.close()

        myFile1 = request.FILES.get("preload", None)
        destination = open("/root/SJTUsoso/static/images/preload/" + myFile1.name, 'wb+')  # 打开特定的文件进行二进制的写操作
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
        destination = open("/root/SJTUsoso/static/images/wechat/" + myFile.name,
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

def words_post(request):
    if request.method == 'POST':
        content = request.POST.get('words', '')
        words_list = content.split(",")
        with open(r"/root/SJTUsoso/static/data/words.json", "w") as f:
            json.dump(words_list, f)
        return HttpResponse("关键词更新成功")
    else:
        return HttpResponse("程序错误，请回退重试")

def user_cluster(request):
    results = kmeans_cluster ()
    users = {}
    tag = list(Video.objects.values_list("tag"))
    tag_diff = list(set(tag))

    for i in range(len(results)):
        if (i%2==0):
            scores = results[i+1]
            tag_scores={}
            for j in range(len(tag)):
                tag_scores[tag[j]]=scores[j]
            dict_category={}
            for elem in tag_diff:
                for k in tag_scores.keys():
                    if k==elem:
                        if k in dict_category.keys():
                            dict_category[k]+=tag_scores[k]
                        else:
                            dict_category[k] = tag_scores[k]
            users[results[i]]=dict_category
    return render(request, "user/cluster.html", {"title": "欢迎来到用户聚类界面","users": users})

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
    all_comments = VideoComments.objects.values("user_nickname","content","id")
    with open(r"/root/SJTUsoso/static/data/words.json", 'r') as load_f:
        load_list = json.load(load_f)
    comments={}
    for i in range(len(all_comments)):
        for elem in load_list:
            if elem in all_comments[i]["content"]:
                comments[all_comments[i]["id"]]=all_comments[i]["user_nickname"]+":"+all_comments[i]["content"]
                break
    return render(request, "user/check_comment.html", {"title": "欢迎来到评论监管界面","comments":comments})

def to_del_comment(request,comment_id):
    VideoComments.objects.get(id=comment_id).delete()
    all_comments = VideoComments.objects.values("user_nickname", "content", "id")
    with open(r"/root/SJTUsoso/static/data/words.json", 'r') as load_f:
        load_list = json.load(load_f)
    comments = {}
    for i in range(len(all_comments)):
        for elem in load_list:
            if elem in all_comments[i]["content"]:
                comments[all_comments[i]["id"]] = all_comments[i]["user_nickname"] + ":" + all_comments[i]["content"]
                break
    return render(request, "user/check_comment.html", {"title": "欢迎来到评论监管界面", "comments": comments})