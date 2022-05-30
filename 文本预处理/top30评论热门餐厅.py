# 1. 热门美食和美食品牌、美食旅游目的地识别
import pandas as pd

d1 = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/【携程】广州粤菜餐厅.xlsx')
d2 = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/去哪儿网-广州粤菜餐厅.xlsx')
d1_sorted = d1.sort_values("评论数量", ascending=False)
d2_sorted = d2.sort_values("评论数量", ascending=False)
d1_ranking = d1_sorted.iloc[:30, [0, 2]]
d2_ranking = d2_sorted.iloc[:30, [0, 2]]  # 抽选出评论数量排名前三十的餐厅

# 将d2中的商铺名称中的英文剔除，观察出d2中商铺名的中英文规律是第一个（）后面就是英文翻译
for i in range(30):
    name = d2_ranking.iloc[i, 0]  # 遍历商铺的每一行
    a = name.find(')')  # 找到第一次出现)的地方
    if a != -1:  # 有括号的话
        d2_ranking.iloc[i, 0] = name[:a+1]

# 对特殊名字分别清理
d2_ranking.iloc[3, 0]= "南信牛奶甜品专家"
d2_ranking.iloc[4, 0]= "海底捞火锅(珠影星光城店)"
d2_ranking.iloc[13, 0]= "宝华面店"
d2_ranking.iloc[24, 0]= "陶陶居饼家"

# 算出合并后的店铺评论数量排名top30
d3_ranking = pd.merge(left = d1_ranking, right= d2_ranking, left_on='餐厅', right_on="商铺", how='outer')  # 将横行表全合并
d3_ranking.loc[:, ['评论数量_x', '评论数量_y']]= d3_ranking.loc[:,['评论数量_x', '评论数量_y']].fillna(0)  # 将评论数量为null转化成0
d3_ranking['评论总量']= d3_ranking.loc[:, '评论数量_x']+d3_ranking.loc[:, '评论数量_y']  # 算出评论总量
final_ranking = d3_ranking.sort_values("评论总量", ascending=False).head(30)
final_ranking.to_excel('/Users/liyuxiao/Desktop/毕业论文/火热店铺评论数量排名top30.xlsx')


