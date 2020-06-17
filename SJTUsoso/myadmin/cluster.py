from sklearn.cluster import KMeans
import numpy as np
import MySQLdb
def kmeans_cluster():
    db = MySQLdb.connect("localhost", "root", "123", "sjtusoso", charset='utf8' )
    cursor = db.cursor()

    cursor.execute("SELECT count(*) from blog_user")
    user_num = cursor.fetchall()[0][0]
    cursor.execute("SELECT count(*) from blog_video")
    video_num = cursor.fetchall()[0][0]

    x=[]
    for i in range(user_num): #每一个用户查询一次
        user_id = str(i + 1)
        sql = "SELECT mark,video_id,user_id from blog_rate where user_id = %s" % user_id
        cursor.execute(sql)
        data = cursor.fetchall()

        tmp = {}  # 所有打分的视频列表
        for k in data:
            tmp[k[1]]=k[0]

        #print(tmp)
        tmp2 = [] #添加到输入中
        for j in range(video_num):
            if (j+1) not in tmp.keys():
                tmp2.append(0)
            else:
                tmp2.append(tmp[j+1])
        x.append(tmp2)

    dict_nickname={}
    sql = "SELECT id,nickname from blog_user"
    cursor.execute(sql)
    data = cursor.fetchall()
    for t in data:
        dict_nickname[t[0]]=t[1]

    X=np.array(x)
    kmeans = KMeans(n_clusters=3, random_state=0).fit(X)

    results=[]
    for i in range(len(kmeans.cluster_centers_)):
        tmp = [] #取出id
        for j in range(len(kmeans.labels_)):
            if  kmeans.labels_[j]==i:
                tmp.append(j+1)
        tmp2 = [] #替换为Nickname
        for m in tmp:
            tmp2.append(dict_nickname[m])

        round_list = [round(elem, 2) for elem in kmeans.cluster_centers_[i]]
        results.append("相似用户："+str(tmp2))
        results.append("簇心：" + str(round_list))

    db.close()
    return results

if __name__ == '__main__':
    kmeans_cluster()