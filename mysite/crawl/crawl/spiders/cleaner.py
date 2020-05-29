# -*- coding: utf-8 -*-
import re

def fmt_text(text):
    text = re.sub('\s*\n\s*', '', text.strip())                      # spaces
    text = re.sub('[ \f\r\t　]+', '', text)
    text = re.sub('&(nbsp|e[mn]sp|amp|thinsp|zwn?j|#13);', ' ', text)
    text = re.sub('\xa0|\u3000|\\\\xa0|\\\\u3000', ' ', text)
    text = re.sub('\[\]|【】|（）|\(\)|{}|<>|“”|‘’|◆', '', text)       # brackets
    text = text.replace('【', '（').replace('】', '）')
    text = re.sub('"([\s\S]*?)"', lambda x: "“" + x.group(1) + "”", text)   
    text = re.sub('[.]{3,}|,{3,}|。{3,}|，{3,}|…+', '…', text)        # ellipses
    text = re.sub('(?<=[\u4e00-\u9fa5])\((?=[\u4e00-\u9fa5])', '（', text)   # to full-width
    text = re.sub('(?<=[\u4e00-\u9fa5])\)(?=[\u4e00-\u9fa5])', '）', text)
    text = re.sub('(?<=[\u4e00-\u9fa5])[,，]+(?=[\u4e00-\u9fa5])', '，', text)
    text = re.sub('(?<=[\u4e00-\u9fa5])[.。]+(?=[\u4e00-\u9fa5])', '。', text)
    text = re.sub('(?<=[\u4e00-\u9fa5])[:：]+(?=[\u4e00-\u9fa5])', '：', text)
    text = re.sub('(?<=[\u4e00-\u9fa5])[;；]+(?=[\u4e00-\u9fa5])', '；', text)
    text = re.sub('(?<=[\u4e00-\u9fa5])[!！]+(?=[\u4e00-\u9fa5])', '！', text)
    text = re.sub('(?<=[\u4e00-\u9fa5])[?？]+(?=[\u4e00-\u9fa5])', '？', text)
    return text
