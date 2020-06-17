import os
import random
import math
import json
import re
import hashlib
from functools import wraps
from urllib.parse import urlencode

from django.db.models import Avg, Q, Count, F
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from rest_framework.renderers import JSONRenderer

from SJTUsoso import settings
from SJTUsoso.utils import *
from soso import models as sosomodels
from blog.models import Wechat, Video, User, Rate, VideoComments, MessageBoard, CollectBoard, BoardComment
from . import models
from .forms import *
from .ucf import ItemBasedCF
from .recom_friend import *
from .one_tfidf import *


# Create your views here.
def tocategory(request):
    return render(request, 'category.html')


def login(request):
    if request.session.get('is_login', None):
        return redirect('home')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['nickname'] = user.nickname
                    return redirect('home')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

# def login_in(func):  # 验证用户是否登录
#   @wraps(func)
#   def wrapper(*args, **kwargs):
#       request = args[0]
#       is_login = request.session.get("login_in")
#       print(is_login)
#       if is_login:
#           return func(*args, **kwargs)
#       else:
#           return redirect(reverse("login"))
#
#   return wrapper


def message_boards(request, fap_id=1, pagenum=1, **kwargs):
    # 获取论坛内容
    msg = request.GET.get('msg', '')
    # print('做了缓存')
    have_board = True
    if fap_id == 1:
        # 热门
        msg_board = MessageBoard.objects.all().order_by('-like_num')
    elif fap_id == 2:
        # 最新
        msg_board = MessageBoard.objects.all().order_by('-create_time')
    elif fap_id == 3:
        # 点赞
        try:
            user = User.objects.get(name=request.session['user_name'])
            collectboards = CollectBoard.objects.filter(user=user, is_like=True).order_by(
                'create_time')
            msg_board = []
            for mb in collectboards:
                msg_board.append(mb.message_board)
        except:
            return render(request, "index.html", locals())

    elif fap_id == 4:
        # 收藏
        try:
            user = User.objects.get(name=request.session['user_name'])
            collectboards = CollectBoard.objects.filter(user=user, is_collect=True).order_by(
                'create_time')
            msg_board = []
            for mb in collectboards:
                msg_board.append(mb.message_board)
        except:
            return render(request, "index.html", locals())

    elif fap_id == 5:
        # 我的
        try:
            user = User.objects.get(name=request.session['user_name'])
            msg_board = MessageBoard.objects.filter(user=user).order_by('-create_time')
        except:
            return render(request, "index.html", locals())
    else:
        msg_board = MessageBoard.objects.all().order_by('create_time')
    if not msg_board:
        have_board = False

    # 构建分页器对象,blogs=所有博文,2=每页显示的个数
    paginator = Paginator(msg_board, 10)

    # 获取第n页的页面对象
    page = paginator.page(pagenum)

    # 构造页面渲染的数据
    '''
    渲染需要的数据:
    - 当前页的博文对象列表
    - 分页页码范围
    - 当前页的页码
    '''
    data = {
        # 当前页的博文对象列表
        "page": page,
        # 分页页码范围
        "pagerange": paginator.page_range,
        # 当前页的页码
        "currentpage": page.number,
        "message_boards": msg_board,
        "have_board": have_board,
        "fap_id": fap_id,
    }
    return render(request, "message_boards.html", context=data)

def new_message_board(request):
    # 写新论坛
    user = User.objects.get(name=request.session['user_name'])
    title = request.POST.get("title")
    content = request.POST.get("content")
    # print('ddddddddddddddddd', title, content)
    if not title or not content:
        return redirect(reverse("message_boards", kwargs={'fap_id': 2, 'pagenum': 1}))
    MessageBoard.objects.create(user=user, content=content, title=title)
    return redirect(reverse("message_boards", args=(2, 1)))

def get_message_board(request, message_board_id, fap_id=1, currentpage=1):
    try:
        user = User.objects.get(name=request.session['user_name'])
        collectboard = CollectBoard.objects.filter(user=user, message_board_id=message_board_id)
        is_like = collectboard.first().is_like
        is_collect = collectboard.first().is_collect
    except:
        is_like = 0
        is_collect = 0

    MessageBoard.objects.filter(id=message_board_id).update(look_num=F('look_num') + 1)
    msg_board = MessageBoard.objects.get(id=message_board_id)
    board_comments = msg_board.boardcomment_set.all()
    have_comment = True
    if not board_comments:
        have_comment = False

    context = {"msg_board": msg_board,
               "board_comments": board_comments,
               "have_comment": have_comment,
               "fap_id": fap_id,
               "currentpage": currentpage,
               'is_like': is_like,
               'is_collect': is_collect,
               'message_board_id': message_board_id
               }

    return render(request, "message_board.html", context=context)

def new_board_comment(request, message_board_id, fap_id=1, currentpage=1):
    # 写评论
    content = request.POST.get("content")
    if not content:
        return redirect(reverse("get_message_board", args=(message_board_id, fap_id, currentpage)))

    MessageBoard.objects.get(id=message_board_id)
    user = User.objects.get(name=request.session['user_name'])

    BoardComment.objects.create(
        user=user, content=content, message_board_id=message_board_id
    )
    MessageBoard.objects.filter(id=message_board_id).update(feebback_num=F('feebback_num') + 1)
    return redirect(reverse("get_message_board", args=(message_board_id, fap_id, currentpage)))

def like_collect(request):

    user = User.objects.get(name=request.session['user_name'])
    message_board_id = request.POST.get("message_board_id")
    like_or_collect = request.POST.get("like_or_collect", None)  # 点赞还是收藏
    is_like = request.POST.get("is_like", None)  # 是否点赞
    is_collect = request.POST.get("is_collect", None)  # 是否收藏
    # print('lllll', like_or_collect, is_like, is_collect)
    if like_or_collect not in ['like', 'collect'] or None in [is_like, is_collect]:
        return JsonResponse(data={'code': 0, 'msg': '参数有误1'})
    try:
        collectboard = CollectBoard.objects.filter(user=user, message_board_id=message_board_id)
        if not collectboard:
            CollectBoard.objects.create(user=user, message_board_id=message_board_id,
                                        is_collect=is_collect if like_or_collect == 'collect' else 0,
                                        is_like=is_like if like_or_collect == 'like' else 0)
            if like_or_collect == 'like':
                if is_like == 0:
                    MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') - 1)
                else:
                    MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') + 1)
            else:
                if is_like == 0:
                    MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') - 1)
                else:
                    MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') + 1)
            return JsonResponse(data={'code': 1, 'msg': '操作成功'})
        collectboard = collectboard.first()
        if like_or_collect == 'like':
            is_collect = collectboard.is_collect
        else:
            is_like = collectboard.is_like
        CollectBoard.objects.filter(user=user, message_board_id=message_board_id).update(is_collect=is_collect,
                                                                                         is_like=is_like)
        if like_or_collect == 'like':
            if is_like == 0:
                MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') - 1)
            else:
                MessageBoard.objects.filter(id=message_board_id).update(like_num=F('like_num') + 1)
        else:
            if is_like == 0:
                MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') - 1)
            else:
                MessageBoard.objects.filter(id=message_board_id).update(collect_num=F('collect_num') + 1)
        return JsonResponse(data={'code': 1, 'msg': '操作成功', 'is_like': is_like, 'is_collect': is_collect})
    except Exception as e:
        print(e)
        return JsonResponse(data={'code': 0, 'msg': '参数有误2'})

def tosingle(req,Wechat_id):
    user = User.objects.get(name=req.session['user_name'])
    demo1 = Wechat.objects.get(id=Wechat_id)
    filename1 = r"D:\venv\SJTUsousou\SJTUsoso\static\data\fenci.json"
    with open(filename1) as file_obj:
        dicts = json.load(file_obj)

    filename2 = "D:\\venv\\SJTUsousou\\SJTUsoso\\static\\data\\"  + str(user.id) + ".json"
    if not os.path.exists(filename2):
        user_dict={}
        for i in dicts[str(Wechat_id)].keys():
            if i in user_dict.keys():
                user_dict[i]+=dicts[str(Wechat_id)][i]
            else:
                user_dict[i]=dicts[str(Wechat_id)][i]
    else:
        with open(filename2) as file_obj:
            user_dict = json.load(file_obj)
        file_obj.close()
        for i in dicts[str(Wechat_id)].keys():
            if i in user_dict.keys():
                user_dict[i] += dicts[str(Wechat_id)][i]
            else:
                user_dict[i] = dicts[str(Wechat_id)][i]

        user_dict = dict(sorted(user_dict.items(), key=lambda item: item[1], reverse=True))
        count=0
        for i in user_dict.keys():
            count+=1
            if (count>1000):
                del user_dict[i]

    with open(filename2, 'w') as file_obj:
        json.dump(user_dict, file_obj)

    return render(req, 'single.html',{"Wechat": demo1})

def tohome(req):
    try:
        #处理协同过滤视频
        user = User.objects.get(name=req.session['user_name'])
        items = models.Collection.objects.filter(user=user.name)
        itemsum = str(items.count())
        blog_types = models.BlogType.objects.all()
        item = ItemBasedCF()
        item.ItemSimilarity()
        recommedDict = item.Recommend(user.id)
        count = 0
        video_recommend_list=[]
        for k, v in recommedDict.items():
            video_recommend_list.append(k)
            count+=1
            if (count==4):
                break
        num = 4-len(video_recommend_list)
        for i in range(num):
            video_recommend_list.append(random.randint(1,10))

        Videos1 = Video.objects.filter(id__in=[video_recommend_list[0], video_recommend_list[1]])
        Videos2 = Video.objects.filter(id__in=[video_recommend_list[2], video_recommend_list[3]])

        #处理内容推送
        filename = r"D:\venv\SJTUsousou\SJTUsoso\static\data\fenci.json"
        with open(filename) as file_obj:
            dicts = json.load(file_obj)

        filename = "D:\\venv\\SJTUsousou\\SJTUsoso\\static\\data\\"+str(user.id)+".json" #改成user.id
        if not os.path.exists(filename):
            result_id=[random.randint(1,10),random.randint(1,10),random.randint(1,10),random.randint(1,10)]
        else:
            with open(filename) as file_obj:
                user_dict = json.load(file_obj)
            result_dict = {}
            for i in dicts.keys():
                result_dict[i] = cal(dicts[i], user_dict)
            result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1], reverse=True))
            count = 0
            result_id = []
            for i in result_dict.keys():
                count += 1
                result_id.append(int(i)+1)
                if count == 4:
                    break
        Wechats = Wechat.objects.filter(id__in=result_id)
        #处理好友推荐
        friends_id = search_friend(user.id)
        friends = []
        for id in friends_id:
            friends.append((User.objects.get(id=id)).nickname)
    except:
        pass

    try:
        latest_msg_board0 = MessageBoard.objects.order_by('-create_time')[0]
        latest_msg_board1 = MessageBoard.objects.order_by('-create_time')[1]
        latest_msg_board2 = MessageBoard.objects.order_by('-create_time')[2]
        latest_msg_board3 = MessageBoard.objects.order_by('-create_time')[3]
    except:
        pass

    return render(req, "index.html", locals())

def cal(dict1,dict2):#分词与TFIDF处理后的相似度计算
    sum=0
    for key in dict1.keys():
        if key in dict2.keys():
            sum+=dict1[key]*dict2[key]
    return sum

def score(request, Video_id):
    # 打分
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("home")

    user = User.objects.get(id=request.session.get("user_id"))
    video = Video.objects.get(id=Video_id)
    score = float(request.POST.get("score", 0))
    is_rate = Rate.objects.filter(video=video, user=user).first()
    if not is_rate:
        video.rate_num += 1
        video.save()
        video.avg=(video.avg+score)/video.rate_num
        video.save()
        Rate.objects.get_or_create(user=user, video=video, defaults={"mark": score})
        is_rate = {'mark': score}

    return render(request, "detail.html", {"Video":video,"is_rate":is_rate})

def tovideo(req,Video_id):
    demo = Video.objects.get(id=Video_id)
    comments=VideoComments.objects.filter(video_id=Video_id)
    return render(req, 'detail.html',{"Video":demo,"comments":comments})


def login(request):
    if request.session.get('is_login', None):
        return redirect('home')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == hash_code(password):  # 哈希值和数据库内的值进行比对
                    blogs = models.Blog.objects.filter(author=username)
                    blogsnum = str(blogs.count())
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    request.session['nickname'] = user.nickname
                    request.session['myblogs'] = blogsnum
                    return redirect('home')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login.html', locals())

    login_form = UserForm()
    return render(request, 'login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("home")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            #sex = register_form.cleaned_data['sex']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # 用户名唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  # 邮箱地址唯一
                    message = '该邮箱地址已被注册，请使用别的邮箱！'
                    return render(request, 'register.html', locals())
                # 当一切都OK的情况下，创建新用户
                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = hash_code(password1)  # 使用加密密码
                new_user.email = email
                #new_user.sex = sex
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'register.html', locals())

def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("home")
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect("home")

def hash_code(s, salt='mysite'):# 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()

def userspace(request):
    blog_types = models.BlogType.objects.all()
    if "user" in request.GET:
        user = models.User.objects.get(name=request.GET['user'])
        blogs = models.Blog.objects.filter(author=user.name)
        blogsnum = str(blogs.count())
        items = models.Collection.objects.filter(user=user.name)
        itemsum = str(items.count())
        return render(request, 'other.html', locals())
    elif request.session.get('is_login', None):
        user = models.User.objects.get(name=request.session['user_name'])
        items = models.Collection.objects.filter(user=user.name)
        itemsum = str(items.count())
        change = 0
        return render(request, 'user.html', locals())
    else:
        return redirect('/login/')

def userspacechange(request):
    blog_types = models.BlogType.objects.all()
    if request.session.get('is_login', None):
        user = models.User.objects.get(name=request.session['user_name'])
        blogs = models.Blog.objects.filter(author=user.name)
        blogsnum = str(blogs.count())
        if request.method == "POST":
            Userspace_form = UserspaceForm(request.POST)
            message = "请检查填写的内容！"
            if Userspace_form.is_valid():  # 获取数据
                nickname = Userspace_form.cleaned_data['nickname']
                phone = Userspace_form.cleaned_data['phone']
                sex = Userspace_form.cleaned_data['sex']
                intro = Userspace_form.cleaned_data['intro']
                if nickname:
                    user.nickname = nickname
                else:
                    pass
                user.phone = phone
                user.sex = sex
                user.intro = intro
                user.save()
                request.session.flush()
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['nickname'] = user.nickname
                request.session['myblogs'] = blogsnum
                return redirect('/userspace/')
        change = 1
        Userspace_form = UserspaceForm()
        return render(request, 'user.html', locals())
    else:
        return redirect('/login/')

def avatarup(request):
    blog_types = models.BlogType.objects.all()
    if request.session.get('is_login', None):
        user = models.User.objects.get(name=request.session['user_name'])
        blogs = models.Blog.objects.filter(author=user.name)
        blogsnum = str(blogs.count())
        if request.method == "POST":
            avatar_form = UpdateAvatarForm(request.POST, request.FILES)
            message = "请检查上传的图片！"
            if avatar_form.is_valid():
                image = avatar_form.cleaned_data["img"]
                user.img_url = image
                user.save()
                request.session.flush()
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['nickname'] = user.nickname
                request.session['myblogs'] = blogsnum
                return redirect('/userspace/')
        avatar_form = UpdateAvatarForm()
        hide = 1
        return render(request, 'user.html', locals())
    else:
        return redirect('/login/')

def forgot(req):
    return render(req, 'forgot.html')

# def reset(req):
#     return render(req, 'reset.html')

def reset(request):
    if request.session.get('is_login', None):
        if request.method == "POST":
            message = "请检查填写的内容！"
            password1 = request.POST.get('oldpassword', None)
            password2 = request.POST.get('newpassword', None)
            user = models.User.objects.get(name=request.session['user_name'])
            if user.password == hash_code(password1):  # 哈希值和数据库内的值进行比对
                user.password = hash_code(password2)
                user.save()
                return redirect('/logout/')
            else:
                message = "密码错误"
                return render(request, 'reset.html', locals())
        return render(request, 'reset.html')
    return redirect('/login/')

def WBlog(request):
    if request.session.get('is_login', None):
        user = models.User.objects.get(name=request.session['user_name'])
        if request.method == "POST":
            wblog_form = WBlogForm(request.POST, request.FILES)
            message = "请检查文章内容！"
            if wblog_form.is_valid():
                blog_user = user
                title = wblog_form.cleaned_data["title"]
                blog_type = request.POST.get("blog_type", None)
                content = wblog_form.cleaned_data["content"]
                #img_url = wblog_form.cleaned_data["img_url"]

                new_blog = models.Blog.objects.create()
                new_blog.author = blog_user.name
                new_blog.blog_type = blog_type
                new_blog.title = title
                new_blog.content = content
                #new_blog.img_url = img_url
                new_blog.save()
                new_article = sosomodels.SosoSitearticle.objects.create()
                new_article.title = title
                new_article.text = content
                new_article.url = '/blog/'+str(new_blog.pk)+'/'
                new_article.save()
                blogs = models.Blog.objects.filter(author=user.name)
                blogsnum = str(blogs.count())
                request.session.flush()
                request.session['is_login'] = True
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                request.session['nickname'] = user.nickname
                request.session['myblogs'] = blogsnum
                request.session['new_blog'] = new_blog.pk
                return redirect('/blog/'+str(new_blog.pk)+'/')
        blog_types = models.BlogType.objects.all()
        wblog_form = WBlogForm()
        return render(request, 'bwrite.html', locals())
    else:
        return redirect('/login/')

def coverup(request):
    blog_types = models.BlogType.objects.all()
    if request.session.get('is_login', None):
        new_blog = models.Blog.objects.get(pk=request.session['new_blog'])
        del request.session['new_blog']
        if request.method == "POST":
            cover_form = UploadCoverForm(request.POST, request.FILES)
            message = "请检查上传的图片!"
            if cover_form.is_valid():
                cover = cover_form.cleaned_data['img']
                new_blog.img_url = cover
                new_blog.save()
                return redirect('/blog/'+str(new_blog.pk)+'/')
        return redirect('home')
    else:
        return redirect('/login/')

def blog_list(request):
    context = {}
    context['hotest_blog'] = models.Blog.objects.order_by('-like_num')[0]
    context['hot_blogs'] = models.Blog.objects.order_by('-like_num')[1:6:1]
    if "typename" in request.GET:
        blogs = models.Blog.objects.filter(blog_type=request.GET['typename'])
        typename = request.GET['typename']
        context["typename"] = typename
        context["blog_types"] = BlogType.objects.all()
        context["blogs"] = blogs.order_by("-created_time")
        return render(request, 'category.html', context)
    elif "user" in request.GET:
        blogs = models.Blog.objects.filter(author=request.GET['user'])
        user = models.User.objects.get(name=request.GET['user'])
        context["user"] = user
        context["blog_types"] = BlogType.objects.all()
        context["blogs"] = blogs.order_by("-created_time")
        blogs = models.Blog.objects.filter(author=user.name)
        blogsnum = str(blogs.count())
        context["blogsnum"] = blogsnum
        items = models.Collection.objects.filter(user=request.GET['user'])
        context["itemsum"] = str(items.count())
        if request.session.get('is_login', None):
            if request.GET['user'] == request.session['user_name']:
                return render(request, 'myblogs.html', context)
            else:
                pass
        return render(request, 'userblogs.html', context)
    else:
        blogs = models.Blog.objects.all()
        blogs = blogs.order_by("-created_time")
        paginator = Paginator(blogs, 6, 2)  # Show 8 contacts per page
        page = request.GET.get('page')
        try:
            pnumber = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            pnumber = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            pnumber = paginator.page(paginator.num_pages)
        context['max_left_item_count'] = '2'
        context["blogs"] = pnumber#.order_by("-created_time")
        context["blog_types"] = models.BlogType.objects.all()
        #context["blogs"] = blogs.order_by("-created_time")
        return render(request,'category.html',context)

def deblog(request):
    if request.session.get('is_login', None):
        if "key" in request.GET:
            key = request.GET["key"]
            old_blog = models.Blog.objects.get(pk=int(key))
            old_blog.delete()
            blogs = models.Blog.objects.filter(author=request.session['user_name'])
            blogsnum = str(blogs.count())
            request.session['myblogs'] = blogsnum
            messages.success(request, "删除成功!")
        return redirect('/blog/?user='+request.session['user_name'])
    return redirect('/login/')

def blog_detail(request, blog_pk):
    context = {}
    blog = get_object_or_404(models.Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    context['previous_blog'] = models.Blog.objects.filter(created_time__gt=blog.created_time).last()
    context['next_blog'] = models.Blog.objects.filter(created_time__lt=blog.created_time).first()
    context["blog_types"] = models.BlogType.objects.all()
    context["newest_blog"] = models.Blog.objects.latest('pk')
    context["new_blogs"] = models.Blog.objects.order_by('-created_time')[1:4:1]
    context['blog'] = blog
    author = models.User.objects.get(name=blog.author)
    context['author'] = author
    cover_form = UploadCoverForm()
    context['cover_form'] = cover_form
    if request.session.get('is_login', None):
        collection = models.Collection.objects.filter(user=request.session['user_name'], itemtype='blog')
        for item in collection:
            if item.itempk == str(blog.pk):
                context['item'] = item.pk
                break
    response = render(request, 'single1.html', context)
    response.set_cookie(read_cookie_key,'true')
    return response

def collect(request):
    if request.session.get('is_login', None):
        if "key" in request.GET:
            key = request.GET["key"].split("-", 1)
            itemtype = key[0]
            pk = key[1]
            if itemtype == 'blog':
                items = models.Collection.objects.filter(user=request.session['user_name'], itemtype='blog')
                pks = []
                item = models.Blog.objects.get(pk=int(pk))
                for i in items:
                    pks.append(i.itempk)
                if pk in pks:
                    messages.error(request, "已在收藏夹中!")
                    return redirect('/blog/'+str(item.pk)+'/')
                else:
                    new_item = models.Collection.objects.create()
                    new_item.itemtype = 'blog'
                    new_item.user = request.session['user_name']
                    new_item.itemtitle = item.title
                    new_item.itempk = pk
                    new_item.save()
                    item.like_num += 1
                    item.save()
                    messages.success(request, "收藏成功!")
                    return redirect('/blog/'+str(item.pk)+'/')
        elif "user" in request.GET:
            context = {}
            user = models.User.objects.get(name=request.GET['user'])
            items = models.Collection.objects.filter(user=request.GET['user'])
            context["user"] = user
            context["items"] = items
            context["itemsum"] = str(items.count())
            blogs = models.Blog.objects.filter(author=request.GET['user'])
            blogsnum = str(blogs.count())
            context["blogsnum"] = blogsnum
            if request.GET['user'] == request.session['user_name']:
                return render(request, 'mycollection.html', context)
            else:
                pass
            return render(request, 'usercollection.html', context)
    else:
        return redirect('/login/')

def decollect(request):
    if request.session.get('is_login', None):
        if "key" in request.GET:
            key = request.GET["key"]
            try:
                old_item = models.Collection.objects.get(pk=int(key))
                itemtype = old_item.itemtype
                itempk = old_item.itempk
                old_item.delete()
            except:
                messages.error(request, "不在收藏夹中!")
                return redirect('/collect/?user='+request.session['user_name'])
            if itemtype == 'blog':
                try:
                    item = models.Blog.objects.get(pk=int(itempk))
                except:
                    messages.error(request, "该博客已被删除!")
                    return redirect('/collect/?user=' + request.session['user_name'])
                item.like_num -= 1
                item.save()
                messages.success(request, "取消收藏成功!")
                return redirect('/collect/?user='+request.session['user_name'])
    return redirect('/login/')
