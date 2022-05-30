import urllib.request
import json
import pandas as pd
# import baidu-aip  # 调用失败，报错：Python显示没有该第三方库，转用API调用


# 获取百度AI平台的Access Token
def get_access_token():
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=ihPEegKSXRGidURSjTocE1K9' \
           '&client_secret=KARlGrZZPTAAlcepZmzIocZxs6TWn6Y4'
    headers = ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
                             'Version/14.0.1 Safari/605.1.15 ')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    head = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) ' \
           'Version/14.0.1 Safari/605.1.15 '
    request = urllib.request.Request(host)
    request.add_header('User-Agent', head)
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')
    rdata = json.loads(content)
    return rdata['access_token']


results = []


# 接口接入，注意返回的是json格式数据
def sentiment_classify(text):
    raw = {"text": text}
    data = json.dumps(raw).encode('utf-8')
    AT = get_access_token()
    host = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?charset=UTF-8&access_token=" + AT
    request = urllib.request.Request(url=host, data=data)
    request.add_header('Content-Type', 'application/json')
    response = urllib.request.urlopen(request)
    content = response.read().decode('utf-8')  # content为json格式
    content = json.loads(content)  # json字符串解码成python的字典对象
    items = content["items"][0]
    results.append(items)
    return results


comment = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/情感分析训练文本.xlsx', keep_default_na=False)
comment_list = comment["评论"].tolist()

# 调用情感识别函数，对每一个评论文本进行情感倾向判断
for i in comment_list:
    try:
        sentiment_classify(i)
    except KeyError:
        continue

df = pd.DataFrame(data=results)
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/情感分析结果.xlsx')

positive_list, confidence, negative_list, sentiment = [] * 4
result = results
for i in range(len(result)):
    positive_list.append(result[i]["positive_prob"])
    confidence.append(result[i]["confidence"])
    negative_list.append(result[i]["negative_prob"])
    sentiment.append(result[i]["sentiment"])

a = {"positive_list": positive_list}
b = {"confidence": confidence}
c = {"negative_list": negative_list}
d = {"sentiment": sentiment}
dic = {"positive_list": positive_list, "confidence": confidence, "negative_list": negative_list,
        "sentiment": sentiment}
df = pd.DataFrame.from_dict(dic, orient='index')
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/情感分析结果_转换版.xlsx')
