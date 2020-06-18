import csv
import codecs
from datetime import datetime, timedelta
import random

import sys
import os
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'SJTUsoso.settings'
django.setup()


from soso.models import *
from soso.genKw import get_kw, get_view


# qs = SosoSitearticle.objects.filter(date__range=["2020-01-01", "2020-12-31"]).order_by('-view')[:10]
# print(qs.count())


thedate = datetime(2020, 2, 1)

def get_date():
    global thedate
    if random.random() < 0.9:
        thedate += timedelta(days=-1)
    return thedate


if __name__ == '__main__':
    with codecs.open('article/jwc_mxxstz.csv', 'r', encoding='gb18030') as f:
        reader = csv.reader(f)
        for row in reader:
            id = row[0]
            title = row[1]
            url = row[2]
            cont = row[3].split(',')[:-1]
            cont = " ".join(cont)
            if len(cont) > 1:
                cont = cont[1:]

            content = title + ' ' + cont
            (kw1, kw2, kw3) = get_kw(content)
            view = get_view()
            date = get_date()
            cat = "面向学生通知"

            print(title, date)
            art = SosoSitearticle(title=title, url=url, text=cont, date=date, view=view, category=cat, kw1=kw1[:19], kw2=kw2[:19], kw3=kw3[:19])
            art.save()
            # print(art)
