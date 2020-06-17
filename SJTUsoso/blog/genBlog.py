import random
import json

from generate_class import genModel


class myGenModel(genModel):
    def post_process(self, para_word):
        last_end = -1
        for i, item in enumerate(para_word):
            # Find where to end
            if item in ['[SEP]', '[CLS]', '。', '，', '；', '.']:
                last_end = i
            # Replace words
            if item == '[MASK]' or item == '[UNK]':
                para_word[i] = ''
            elif item == '[CLS]' or item == '[SEP]':
                para_word[i] = '\n'
        # End paragraph at last_end
        if para_word[last_end-1] is not '。':
            para_word[last_end] = '。'
        para_text = ''.join(para_word[:last_end+1]).strip()
        return para_text


def gen_word(lst, empty=0.):
    if random.random() < empty:
        return ''
    return random.choice(lst)


def gen_title():
    lst_ver = ['论', '论', '论', '关于', '关于', '关于', '谈谈', '谈', '谈一谈',
               '说说', '说一说', '聊聊', '聊一聊', '讲讲', '讲一讲',
               '记', '记', '记', '记下', '写写', '写一写', ]
    lst_pre = ['我', '我', '我那', '这', '那', '那', '一些', ]
    lst_adj = ['美丽的', '可爱的', '蓬勃的', '感人的', '动人的', '璀璨的',
               '轻快的', '晶莹的', '淡淡的', '匆匆的', '碌碌的', '茫茫的',
               '逝去的', '失去的', '怅然的', '迷惘的', '昔日的', '冷冽的',
               '经历的', '忘却的', '听闻的', '所知道的', '所了解的', '难以置信的',
               '想象中的', '希冀中的', '希望里的', '盼望着的', '热望着的', ]
    lst_nou = ['时光', '流年', '记忆', '年华', '青春', '往年', '岁月',
               '春光', '秋日', '盛夏', '寒冬', '春草', '冬雪', '春夏秋冬',
               '思考', '感想', '想法', '感触', '体悟', '滋味', '随想',
               '母亲', '友人', '爱情', '亲情', '友谊', '倩影', '印象',
               '天空', '大地', '生命', '万物', '永恒', '人间', '人和事',
               '城市', '小城', '乡野', '老屋', '空气', '景色', '景物', ]

    title = gen_word(lst_ver, 0.35) + gen_word(lst_pre, 0.55) + gen_word(lst_adj, 0.35) + gen_word(lst_nou)
    return title


def gen_content(model, title):
    n_ph = random.randint(1, 4)
    temp = random.uniform(0.5, 1.5)
    for i in range(n_ph):
        length = random.randint(80, 350)
        if i == 0:
            intitle = title + '。'
            cont = model.gen_ph(intitle, length=length, temperature=temp-0.3)
            cont = cont[len(intitle):]
        else:
            cont.join(model.gen_ph(length=length, temperature=temp))
    model.clear()
    return cont


def gen_dict(model):
    title = gen_title()
    content = gen_content(model, title)
    return {'title': title, 'content': content}


def file_w(lst, fpath):
    jsn = json.dumps(lst, ensure_ascii=False)
    with open(fpath, 'w', encoding='utf-8') as tf:
        tf.write(jsn)


def file_r(fpath):
    with open(fpath, 'r', encoding='utf-8') as tf:
        jsn = tf.read()
    lst = json.loads(jsn)
    return lst


if __name__ == '__main__':
    # import sys
    # import os
    # from tqdm import tqdm
    # import django

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.append(BASE_DIR)
    #
    # os.environ['DJANGO_SETTINGS_MODULE'] = 'SJTUsoso.settings'
    # django.setup()
    #
    # from blog.models import MessageBoard

    model = myGenModel(model_path='model/prose_pretrain',
        tokenizer_path='model/prose_pretrain/vocab.txt', verbose=1)
    lst = []
    for i in range(3):
        dct = gen_dict(model)
        print(dct['title'])
        print(dct['content'])
        lst.append(dct)

    file_w(lst, 'generated/prose.json')
    # nlst = file_r('generated/prose.json')
    # print(nlst)
