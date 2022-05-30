from random import choice

ls_of_ls = [['广府', '广州', '文化', '海珠区'],
            ['清爽', '脆', '新鲜', '越秀区'],
            ['性价比', '价格',  '消费', '服务员']]
ls_of_words = []  # 存放分词列表（假设是jieba.lcut后得到的）的列表
for i in range(2500):
    ls = choice(ls_of_ls)
    ls_of_words.append([choice(ls) for _ in range(9, 15)])

# 建模训练
from gensim.models import word2vec
import gensim

model = gensim.models.Word2Vec(ls_of_words, vector_size=3, window=7)

# 词向量聚类（基于密度）
from sklearn.cluster import DBSCAN

keys = model.wv.key_to_index.keys()
vectors = []
for key in keys:
    vectors.append(model.wv[key])


labels = DBSCAN(eps=0.24, min_samples=3).fit(vectors).labels_

# 词向量可视化
import matplotlib
from mpl_toolkits import mplot3d
import matplotlib.pyplot as mp

mp.rcParams['font.sans-serif'] = ['Arial Unicode MS']  # 显示中文
matplotlib.rcParams['axes.unicode_minus'] = False  # 显示负号
fig = mp.figure()
ax = mplot3d.Axes3D(fig)  # 创建3d坐标轴
colors = ['red', 'blue', 'green', 'yellow']
for word, vector, label in zip(model.wv.index_to_key, vectors, labels):
    ax.scatter(vector[0], vector[1], vector[2], c=colors[label], s=500, alpha=0.4)
    ax.text(vector[0], vector[1], vector[2], word, ha='center', va='center')
mp.show()
