#!/usr/bin/env python
# -*-coding:utf-8-*-
import math
import pymysql
from blog.models import Rate

class ItemBasedCF:
    def __init__(self):
        # 读取文件，并生成用户-物品的评分表和测试集
        self.train = dict()
        result= Rate.objects.values("mark", "user_id", "video_id")
        for i in result:
            score = i["mark"]
            user = i["user_id"]
            item = i["video_id"]
            self.train.setdefault(user, {})
            self.train[user][item] = int(float(score))
        #print(self.train)

    def ItemSimilarity(self):
        # 建立物品-物品的共现矩阵
        cooccur = dict()  # 物品-物品的共现矩阵
        buy = dict()  # 物品被多少个不同用户购买N
        for user, items in self.train.items():
            for i in items.keys():
                buy.setdefault(i, 0)
                buy[i] += 1
                cooccur.setdefault(i, {})
                for j in items.keys():
                    if i == j: continue
                    cooccur[i].setdefault(j, 0)
                    cooccur[i][j] += 1
        # 计算相似度矩阵
        self.similar = dict()
        for i, related_items in cooccur.items():
            self.similar.setdefault(i, {})
            for j, cij in related_items.items():
                self.similar[i][j] = cij / (math.sqrt(buy[i] * buy[j]))
        #print(self.similar)
        return self.similar

    # 给用户user推荐，前K个相关用户，前N个物品
    def Recommend(self, user, K=10, N=10):
        rank = dict()
        action_item = self.train[user]
        # 用户user产生过行为的item和评分
        for item, score in action_item.items():
            sortedItems = sorted(self.similar[item].items(), key=lambda x: x[1], reverse=True)[0:K]
            for j, wj in sortedItems:
                if j in action_item.keys():
                    continue
                rank.setdefault(j, 0)
                rank[j] += score * wj
        return dict(sorted(rank.items(), key=lambda x: x[1], reverse=True)[0:N])


