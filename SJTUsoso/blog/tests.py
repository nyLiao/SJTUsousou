# import json
# filename = "D:\\venv\\SJTUsousou\\SJTUsoso\\static\\data\\fenci.json"
# with open(filename,'r') as load_f:
#     load_dict = json.load(load_f)
#
# for i in load_dict.keys():
#     print(i)

#coding=utf-8
# 调用文本检测
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
from aliyunsdkgreen.request.extension import HttpContentHelper
import json
import uuid
import datetime

# 请替换成您自己的accessKeyId、accessKeySecret。您可以修改配置文件，也可以直接明文替换
clt = client.AcsClient("您的accessKeyId", "您的accessKeySecret",'cn-shanghai')
region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
request = TextScanRequest.TextScanRequest()
request.set_accept_format('JSON')

task1 = {"dataId": str(uuid.uuid1()),
         "content":"这里填写您要检测的文本",
         "time":datetime.datetime.now().microsecond
        }

# 文本垃圾检测： antispam
request.set_content(HttpContentHelper.toValue({"tasks": [task1], "scenes": ["antispam"]}))
response = clt.do_action_with_exception(request)
print(response)
result = json.loads(response)
if 200 == result["code"]:
    taskResults = result["data"]
    print(taskResults)
    for taskResult in taskResults:
        if (200 == taskResult["code"]):
             sceneResults = taskResult["results"]
             for sceneResult in sceneResults:
                 scene = sceneResult["scene"]
                 suggestion = sceneResult["suggestion"]
                 # 根据scene和suggetion做相关处理
                 # do something
