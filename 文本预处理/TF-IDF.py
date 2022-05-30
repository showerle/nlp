
import pandas as pd
import collections

# pandas默认读取空字符串时读出的是nan，keep_default_na=False参数使读取到空字符串时读出为空：''
clean_list = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/预处理完毕文本.xlsx', keep_default_na=False)
list3 = clean_list.head(5)
null = list3.isnull()
none_null = ~list3[null]
print(none_null.values.tolist())  # 报错 bad operand type for unary ~: 'float'

for i in range(len(clean_list)):
    count = collections.Counter(clean_list[i])
# 下午四点已完成测试collections.Counter(clean_list[1]）测试，没有问题
# 报错key error:0

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
for i, count in enumerate(count_list):  # 遍历每一句话
    scores = {word: tfidf(word, count, count_list) for word in count}  # 以字典格式输出每个单词以及其tfidf的值
    sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)  # 以tfidf的值排倒序输出
    tfidf_list.append(sorted_words)


keywords_list = {}
top_n = 0.35  # 选取top 35%的词作为关键词
for i in range(len(tfidf_list)):
    n = math.floor(top_n * len(tfidf_list[i]))
    keywords_list[i+1] = []
    for j in range(n):
        keywords_list[i+1].append(tfidf_list[i][j])

print(keywords_list)

df = pd.DataFrame.from_dict(keywords_list, orient='index')  # row为key值，列数为最长的values的长度，而其他较短的values则用None填充
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/TFIDF完毕文本_0.35_带TFIDF值.xlsx')

