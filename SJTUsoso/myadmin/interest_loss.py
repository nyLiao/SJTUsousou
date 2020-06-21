import json
import time
def schedule_task():
    filename = "../static/data/fenci.json"
    while (True):
        time.sleep(86400)
        with open(filename, 'r') as file_obj:
            dicts=json.load(file_obj)
        for id in dicts.keys():
            word_dict=dicts[id]
            for word in word_dict.keys():
                word_dict[word]-=0.01
            dicts[id]=word_dict
        with open(filename, 'w') as file_obj:
            json.dump(dicts, file_obj)




