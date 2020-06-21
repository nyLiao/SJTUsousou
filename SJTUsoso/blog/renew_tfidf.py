#coding:utf-8
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import jieba
import codecs
import json
import pymysql

def cal(dict1,dict2):
    sum=0
    for key in dict1.keys():
        if key in dict2.keys():
            sum+=dict1[key]*dict2[key]
    return sum

def tfidf():
    strs = []
    strings = []
    db = pymysql.connect("localhost", "root", "123", "sjtusoso")
    cursor = db.cursor()
    cursor.execute(
        """select content from blog_wechat""")
    results = cursor.fetchall()
    for i in range(len(results)):
        # print(i)
        strings.append(results[i][0])
        strings[i] = ''.join(strings[i].split())

        punct = codecs.open('../static/data/puntuation.txt', 'r', encoding='UTF-8')  # 这是中文标点符号集：排列格式如下图
        punctuation = list()
        for line in punct:
            word = line.strip('\r\n')  # 出去换行符，注意是\r\n
            # word = word.encode('utf-8').decode('utf-8')  # 当然标点符号也需要转换成unicode格式
            punctuation.append(word)
        tmp=""
        for item in strings[i]:
            if item in punctuation:  # 如果是标点符号，即跳过
                continue
            else:
                tmp = tmp + item
        strs.append(' '.join(jieba.cut_for_search(tmp)))
        #print(strs)
    corpus = strs

    def cut(sentence):
        return sentence.split(" ")
    vectorizer = CountVectorizer(analyzer="word", tokenizer=cut)  # 将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i个文本下的词频
    transformer = TfidfTransformer()  # 统计每个词语的tf-idf权值
    X = vectorizer.fit_transform(corpus)
    tfidf = transformer.fit_transform(X)  # 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
    word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
    weight = tfidf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i个文本中的tf-idf权重

    dicts={}
    for i in range(len(weight)):  # 打印每个文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一个文本下的词语权重
        #print("-------这里输出第", i, u"个文本的词语tf-idf权重------")
        dicts[i]={}
        for j in range(len(word)):
            if weight[i][j]!=0:
                dicts[i][word[j]]=weight[i][j]
        dicts[i]=dict(sorted(dicts[i].items(),key=lambda item:item[1],reverse=True) )
    filename = "../static/data/fenci.json"

    cursor.execute(
        """select id from blog_wechat""")
    results = cursor.fetchall()

    cipin_dict = {}
    for i in range(len(dicts)):
        cipin_dict[results[i][0]]= dicts[i]

    with open(filename, 'w') as file_obj:
        json.dump(cipin_dict, file_obj)

if __name__ == "__main__":
    tfidf()


