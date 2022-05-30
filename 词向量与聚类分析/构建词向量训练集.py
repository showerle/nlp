import pandas as pd
import sys
import json
import gensim
from gensim.models import word2vec

# df = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/TFIDF完毕文本_词向量版2.xlsx')
# df.to_csv("/Users/liyuxiao/Desktop/毕业论文/词向量训练集.txt", sep=' ', index=False)
txt = open("/Users/liyuxiao/Desktop/毕业论文/词向量训练集.txt", "r", encoding="utf-8")
txt2 = open("/Users/liyuxiao/Desktop/毕业论文/美食评论文本.txt", "w", encoding="utf-8")

l = []
for line in txt.readlines():
    if line is not None and line != '':
        l.append(line.replace('\n', ''))

results = ' '.join(l)
txt2.write(results)
txt.close()
txt2.close()
