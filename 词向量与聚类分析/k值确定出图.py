import numpy as np
from matplotlib import pyplot as plt

'''
# inertia
plt.plot([i for i in range(3, 10)], [9332, 8190, 5830, 5580, 5201, 4870, 4691],  color='r', marker='o')
# 添加文本 #x轴文本
plt.xlabel('the Number of Cluster')
# y轴文本
plt.ylabel('inertia')
# 标题
plt.title(' the Elbow Method using inertia')
plt.show()
'''

# 轮廓系数
plt.plot([i for i in range(3, 10)], [0.58, 0.60, 0.65, 0.51, 0.49, 0.45, 0.44],  color='b', marker='o')
# 添加文本 #x轴文本
plt.xlabel('the Number of Cluster')
# y轴文本
plt.ylabel('silhouette index')
# 标题
plt.title(' Choosing K-value using Silhouette Score')
plt.show()


'''
# CH指数
plt.plot([i for i in range(3, 10)], [37600, 40535, 47589, 36967, 32899, 29380, 27689],  color='g', marker='o')
# 添加文本 #x轴文本
plt.xlabel('the Number of Cluster')
# y轴文本
plt.ylabel('Calinski-Harabaz Index')
# 标题
plt.title(' Choosing K-value using Calinski-Harabaz Index')
plt.show()
'''