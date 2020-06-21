import MySQLdb
import math
import json
from blog.models import Rate

# 打开数据库连接
def cal(dict1,dict2):
    sum = 0
    count =0
    for key in dict1.keys():
        if key in dict2.keys():
            count+=1
            sum+=(dict1[key]-dict2[key])**2
    return math.sqrt(sum/count)
def cal2(dict1,dict2):
    sum=0
    for key in dict1.keys():
        if key in dict2.keys():
            sum+=dict1[key]*dict2[key]
    return sum

def search_friend(user_id):
    result = Rate.objects.values("mark", "user_id", "video_id")
    dict1 = {}
    for i in result:
        score = i["mark"]
        user = i["user_id"]
        video = i["video_id"]
        if user not in dict1.keys():
            dict1[user] = {}
            dict1[user][video] = score
        else:
            dict1[user][video] = score

    user_data = dict1[user_id]
    dict2={}
    try:
        with open('./static/data/'+str(user_id)+'.json', 'r', encoding='utf8')as fp:
            data1 = json.load(fp)
    except:
        pass
    for i in dict1.keys():
        if i !=user_id:
             op_data = dict1[i]
             tmp1= cal(user_data,op_data)
             try:
                  with open('./static/data/'+str(i)+'.json', 'r', encoding='utf8')as fp:
                       data2 = json.load(fp)
                  tmp2 = cal2(data2, data1)
             except:
                  tmp2=0
             dict2[i]=  (tmp2+1) / (tmp1+1)

    user_dict = dict(sorted(dict2.items(), key=lambda item: item[1], reverse=True))
    return (list(user_dict.keys()))




