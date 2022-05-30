from gensim.models import word2vec
from sklearn.cluster import KMeans
import numpy as np
from matplotlib import pyplot as plt
from sklearn import metrics

# 加载模型
model = word2vec.Word2Vec.load("美食评论文本.model")
# print(model.wv.most_similar("性价比", topn = 20))


# 获取model里面的所有关键词
keys = model.wv.key_to_index.keys()
# print(keys)
# print(type(keys))
# print(list(keys)[0])
# print(model.wv['岭南'])


# 获取词对应的词向量
wordvector = []
for key in keys:
    wordvector.append(model.wv[key])

# 转为单位向量
uv = np.linalg.norm(wordvector.vectors, axis=1).reshape(-1, 1)  # uv为Unit Vector
wordvector.vectors = wordvector.vectors / uv  # Vector or matrix norm


# 输出指标函数km，classCount为分类数
def km(classCount):
    clf = KMeans(n_clusters=classCount)
    kmeans_model = clf.fit(wordvector)
    # 获取每个聚类中心 
    # centers = clf.cluster_centers_
    # 预测结果
    # result = clf.predict(wordvector)
    # return metrics.silhouette_score(wordvector, result)
    # return clf.inertia_
    labels = kmeans_model.labels_
    return metrics.calinski_harabasz_score(wordvector, labels)


y = []
for i in range(3, 11):
    y.append(km(i))

plt.plot([i for i in range(3, 11)], y, color='r', marker='o')
# 添加文本 #x轴文本
plt.xlabel('the number of cluster')
# y轴文本
plt.ylabel('ch')
# 标题
plt.title('Calinski-Harabaz Index')
plt.show()

'''
# 模型训练
clf = KMeans(n_clusters=3)
clf.fit(wordvector)
# 获取每个聚类中心
centers = clf.cluster_centers_
# 预测结果
result = clf.predict(wordvector)
# 用不同的颜色绘制数据点
mark = ['or', 'og', 'ob']
for i, d in enumerate(wordvector):
    plt.plot(d[0], d[1], mark[result[i]])
# 画出各个分类的中心点
mark = ['*r', '*g', '*b']
for i, center in enumerate(centers):
    plt.plot(center[0], center[1], mark[i], markersize=40)

plt.show()
'''

'''
# 获取到所有词向量所属类别 
labels = clf.labels_
# print('类别：',labels)
# print(type(labels))

# 把是一类的放入到一个字典里
classCollects = {}
for i in range(len(keys)):

    # print('len(keys):',len(keys))#长度
    # print('classCollects的keys:',classCollects.keys())
    # print('labels[i]',labels[i])
    # print(keys)
    # print('dict_keys:',list(keys)[0])#将dict_keys转换为list，输出第一个元素
    # print(type(classCollects.keys()))
    # print(type(classCollects))

    # print(i)
    # print(classCollects.keys())
    print(list(classCollects.keys()))

    if labels[i] in list(classCollects.keys()):
        classCollects[labels[i]].append(list(keys)[i])
    else:
        classCollects={0:[],1:[],2:[],3:[],4:[], 5:[],6:[],7:[],8:[],9:[]}


print('0类：',classCollects[0])
print('1类：',classCollects[1])
print('2类：',classCollects[2])
print('3类：',classCollects[3])
print('4类：',classCollects[4])
print('5类：',classCollects[5])
print('6类：',classCollects[6])
print('7类：',classCollects[7])
print('8类：',classCollects[8])
print('9类：',classCollects[9])


# 转换为字典格式报错并输出
a = {}
for i in range(10):
    a[i] = classCollects[i]

df = pd.DataFrame.from_dict(a, orient='index')
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/分类结果1.xlsx')
'''
