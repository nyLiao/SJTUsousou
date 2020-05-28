# import json
import simplejson as json
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from haystack.query import SearchQuerySet

from SJTUsoso import settings
from SJTUsoso.utils import *
from .models import *

from haystack.views import SearchView

# Create your views here.

def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # print(suggestions)
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
    
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

def tocontact(req):
    return render(req, 'contact.html')

def tocategory(req):
    return render(req, 'category.html')

def tosingle(req):
    return render(req, 'single.html')

def to403(req):
    return render(req, '403.html')

def to404(req):
    return render(req, '404.html')

def to500(req):
    return render(req, '500.html')

def to503(req):
    return render(req, '503.html')

def topage(req):
    return render(req, 'page.html')
