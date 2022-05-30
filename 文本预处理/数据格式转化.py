import pandas as pd
import numpy as np

d1 = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/【携程】广州粤菜餐厅.xlsx')
d2 = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/去哪儿网-广州粤菜餐厅.xlsx')

'''
报错记录：single positional indexer is out - of - bounds
报错原因：list读取超出索引值，即越界
'''

comment_list = []
# 将d1的评论文本提取出来
for i in range(1503):
    for j in range(7, 27):
        if ~pd.isnull(d1.iloc[i, j]):
            comment_list.append(d1.iloc[i, j])
        else:
            continue

# 将d2的评论文本提取出来
for i in range(1989):
    for j in range(4, 24):
        if ~pd.isnull(d2.iloc[i, j]):
            comment_list.append(d2.iloc[i, j])
        else:
            continue

# 用numpy再次对新生成对列表去重
while np.nan in comment_list:
    comment_list.remove(np.nan)


#将comment_list输出为原始文本评论合集
# df = pd.DataFrame(index=[i+1 for i in range(len(comment_list))], data=comment_list)
# df.to_excel('/Users/liyuxiao/Desktop/毕业论文/原始文本评论合集.xlsx')


# 去掉文本中的空格
def remove_blank(our_data):
    m1 = map(lambda s: s.replace(' ', ''), our_data)
    return list(m1)


# 让文本只保留汉字
def is_chinese(uchar):
    if u'\u4e00' <= uchar <= u'\u9fa5':
        return True
    else:
        return False


def format_str(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str = content_str + i
    return content_str


# 参函数传入的是每一句话
chinese_list = []
for line in comment_list:
    chinese_list.append(format_str(line))

# 对文本进行jieba分词
import jieba

jieba.setLogLevel(jieba.logging.INFO)


def sentence_word(datas):
    cut_words = map(lambda s: list(jieba.cut(s)), datas)
    return list(cut_words)


word_list = sentence_word(chinese_list)

# 将停用词表转化为list格式
fr = open("/Users/liyuxiao/Desktop/毕业论文/stopwords.txt", "r")
stopwords = [str(x) for x in fr.read().split()]


# 去掉文本中的停用词
def drop_stopwords(contents, stopwords):
    contents_clean = []
    for line in contents:
        line_clean = []
        for word in line:
            if word in stopwords:
                continue
            line_clean.append(word)
        contents_clean.append(line_clean)
    return contents_clean


# 预处理完成
clean_list = drop_stopwords(word_list, stopwords)

# 统计得出一共有1462244个词
word_num = 0
for i in clean_list:
    for j in i:
        word_num += len(j)
print(word_num) 


# 将预处理完成的数据保存成csv.
# clean_list2 = pd.DataFrame(index=[i for i in range(len(clean_list))], data=clean_list)
# clean_list2.to_excel('/Users/liyuxiao/Desktop/毕业论文/预处理完毕文本.xlsx')


import collections
# 统计词频
count_list = []
for i in range(len(clean_list)):
    count = collections.Counter(clean_list[i])  # Counter函数可以统计每个字符在该句子里出现的个数
    count_list.append(count)  # count是每一个句子里词与其词频的健值对组成的字典


# count[word]可以得到每个单词的词频<—由Counter函数统计得到
# sum(count.values())得到整个句子的单词总数
def tf(word, count):
    return count[word] / sum(count.values())


# 统计的是含有该单词的句子数
def n_containing(word, count_list):
    return sum(1 for count in count_list if word in count)


# len(count_list)是指句子的总数，n_containing(word, count_list)是指含有该单词的句子的总数，加1是为了防止分母为0
import math


def idf(word, count_list):
    return math.log(len(count_list) / (1 + n_containing(word, count_list)))


# 将tf和idf相乘
def tfidf(word, count, count_list):
    return tf(word, count) * idf(word, count_list)


# 输出每个词以及其TF_IDF值
tfidf_list = []
words = []
for i, count in enumerate(count_list):  # 遍历每一句话
    scores = {word: tfidf(word, count, count_list) for word in count}  # 以字典格式输出每个单词以及其tfidf的值
    words.append(scores)
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)  # 以tfidf的值排倒序输出
    tfidf_list.append(sorted_words)

# 此次注意1、字典是unhashable，只能通过key找value 2、x.values()得到的是'dict_values'类型，需要进行类型转化
words = sorted(words, key=lambda x: str(list(x.values())), reverse=True)
df = pd.DataFrame(words)
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/单词以及其TFIDF值.xlsx')


keywords_list = {}
top_n = 0.35  # 选取top 80%的词作为关键词
for i in range(len(tfidf_list)):
    n = math.floor(top_n * len(tfidf_list[i]))
    keywords_list[i+1] = []
    for j in range(n):
        keywords_list[i+1].append(tfidf_list[i][j])

# print(keywords_list)
df = pd.DataFrame.from_dict(keywords_list, orient='index')  # row为key值，列数为最长的values的长度，而其他较短的values则用None填充
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/TFIDF完毕文本_0.35_带TFIDF值.xlsx')

'''
报错记录：字典转DataFrame结果报错arrays must all be same length
错误原因：把不等长的value输出
'''

# df = pd.DataFrame.from_dict(keywords_list, orient='index')  # row为key值，列数为最长的values的长度，而其他较短的values则用None填充
# df.to_excel('/Users/liyuxiao/Desktop/毕业论文/TFIDF完毕文本.xlsx')
# Excel操作：将TFIDF完毕文本第一列改为原始文本


