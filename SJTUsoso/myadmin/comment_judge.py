#coding=utf-8
from aliyunsdkcore import client
from aliyunsdkcore.profile import region_provider
from aliyunsdkgreen.request.v20180509 import TextScanRequest
#from aliyunsdkgreen.request.extension import HttpContentHelper
import json
import uuid
import datetime
def judge_comment(text):
    scene = ""
    try:
        clt = client.AcsClient("LTAI4G2fE2X92qeebDbbd2x9", "ZgPO4ggLmMANExTptf11YHyQkBhMzy",'cn-shanghai')
        region_provider.modify_point('Green', 'cn-shanghai', 'green.cn-shanghai.aliyuncs.com')
        request = TextScanRequest.TextScanRequest()
        request.set_accept_format('JSON')
        task1 = {"dataId": str(uuid.uuid1()),
                 "content":text,
                 "time":datetime.datetime.now().microsecond
                }
        # 文本垃圾检测
        request.set_content(HttpContentHelper.toValue({"tasks": [task1], "scenes": ["antispam"]}))
        response = clt.do_action_with_exception(request)
        print(response)
        result = json.loads(response)
        if 200 == result["code"]:
            taskResults = result["data"]
            for taskResult in taskResults:
                if (200 == taskResult["code"]):
                     sceneResults = taskResult["results"]
                     for sceneResult in sceneResults:
                         scene = sceneResult["scene"]
    except:
        pass
    return scene
