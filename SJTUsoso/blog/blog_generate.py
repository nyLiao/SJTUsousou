import json
import random

with open ('./data/prose.json','r',encoding='utf-8') as fp:
    json_data = json.load(fp)
    # print(json_data)

import MySQLdb

conn=MySQLdb.connect(
    host='39.100.88.210',
    user='mulval',
    passwd='mulval',
    db='SJTUsoso',
    port=3306,
    charset='gb18030')

cursor = conn.cursor()

test = json_data[0]['content']

def context(test):
    test1 = test.replace('\n','</p><p>')
    test2 = test1[4:]+'</p>'
    return test2

author = ['MekAkUActOR','517021910754','superuser','10','11','1','6']


# for i in range(50):
title = json_data[1]['title']
text = json_data[1]['content']

content = context(text)

id =14

au = random.choice(author)


sql = "INSERT INTO blog_blog(id,author,title,blog_type,content,created_time,last_updated_time,create_month,img_url,like_num) VALUES(%s,'%s','%s','%s','%s','%s','%s','%s','%s',%s);" % (id ,au,title,'散文',content,'2020-06-18 14:34:06.183597','2020-06-18 14:34:06.372609','June','',0)

with open('text.txt', 'w') as target:
    target.write(sql)

cursor.execute(sql)
