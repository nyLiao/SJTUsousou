import numpy as np
import jieba
import jieba.analyse


def distinct(lst):
    """Delete repeat element in list."""
    nlst = []
    for x in lst:
        if x not in nlst:
            nlst.append(x)
    return nlst


def get_kw(content):
    """Get promised top 3 keywords list of content."""
    lst = jieba.analyse.textrank(content, 3, withWeight=False, allowPOS=('ns', 'n', 'vn'))
    if len(lst) < 3:
        lst += jieba.analyse.textrank(content, withWeight=False)
        lst = distinct(lst)[:3]
    else:
        return lst
    if len(lst) < 3:
        lst += jieba.analyse.tfidf(content, withWeight=False)
        lst = distinct(lst)[:3]
    if len(lst) < 3:
        lst += jieba.lcut(content + '上海交通大学')
    lst = distinct(lst)[:3]
    return lst


def set_kw(obj):
    content = obj.title + ' ' + obj.text
    (kw1, kw2, kw3) = get_kw(content)
    obj.kw1 = kw1
    obj.kw2 = kw2
    obj.kw3 = kw3


def get_view():
    v = np.random.normal(500, 300, 1)
    v = v if v > 30 else (np.abs(v) + 30)
    return v


def set_view(obj):
    obj.view = get_view()


if __name__ == '__main__':
    import sys
    import os
    from tqdm import tqdm
    import django

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(BASE_DIR)

    os.environ['DJANGO_SETTINGS_MODULE'] = 'SJTUsoso.settings'
    django.setup()

    from soso.models import SosoSitearticle

    lst = SosoSitearticle.objects.all()

    for article in tqdm(lst):
        if article.kw1 is None:
            # print(article.title + ' ' + article.text)
            set_kw(article)
        # set_view(article)
        article.save()
