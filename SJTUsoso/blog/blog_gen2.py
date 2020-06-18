import csv
import codecs
from datetime import datetime, timedelta
import random
import json

import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'SJTUsoso.settings'
django.setup()

from blog.models import *


with open ('./data/prose.json','r',encoding='utf-8') as fp:
    json_data = json.load(fp)

test = json_data[0]['content']

def context(test):
    test1 = test.replace('\n','</p><p>')
    test2 = test1[4:]+'</p>'
    return test2

author = ['MekAkUActOR','517021910754','superuser','10','11','1','6']


for i in range(50):
    title = json_data[i]['title']
    text = json_data[i]['content']

    content = context(text)

    au = random.choice(author)

    obj = Blog(author=au, title=title, blog_type='散文', content=content, created_time='2020-06-19 04:34:06.183597', last_updated_time='2020-06-19 04:34:06.183597', create_month='June', like_num=0)

    obj.save()
