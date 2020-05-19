from django.shortcuts import render,get_object_or_404, redirect, HttpResponse
from blog.models import *
import json
from django.core.mail import send_mail
from SJTUsoso import settings
from SJTUsoso.utils import *

# Create your views here.

def contactme(req):
    name = req.POST.get('name', None)
    email = req.POST.get('email', None)
    message = req.POST.get('message', None)
    subject = req.POST.get('subject', None)
    if email:
        msg = name + '\n' + email + '\n' + message + '\n'
        send_mail(subject, msg, settings.EMAIL_HOST_USER,
                ['haowenliew@outlook.com'], fail_silently=False)
        return redirect('/contactsuccess/')
    else:
        return redirect('/contactfail/')

def contactsuccess(req):
    return render(req, 'contact.html', {"successmessage":"* The Email was Sent Successfully!"})

def contactfail(req):
    return render(req, 'contact.html')

def tohome(req):
    return render(req, 'index.html')

def tologin(req):
    return render(req, 'login.html')

def toregister(req):
    return render(req, 'register.html')

def tocontact(req):
    return render(req, 'contact.html')

def tocategory(req):
    return render(req, 'category.html')

def toforgot(req):
    return render(req, 'forgot.html')

def toreset(req):
    return render(req, 'reset.html')

def tosingle(req):
    return render(req, 'single.html')

def tosearch(req):
    return render(req, 'search.html')

def to403(req):
    return render(req, '403.html')

def to404(req):
    return render(req, '404.html')

def to500(req):
    return render(req, '500.html')

def to503(req):
    return render(req, '503.html')

def toHome(req):
    return render(req, 'index.html')

def topage(req):
    return render(req, 'page.html')
