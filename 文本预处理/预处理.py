
import pandas as pd
comment = pd.read_excel('/Users/liyuxiao/Desktop/毕业论文/情感分析原始文本.xlsx', keep_default_na=False)
comment_list = comment["评论"]
comment_list = comment_list.tolist()


# 去掉文本中的空格和空行
def remove_blank_row(our_data):
    m1 = map(lambda s: s.replace('\n', ''), our_data)
    return list(m1)


results = remove_blank_row(comment_list)
df = pd.DataFrame(data=results)
df.to_excel('/Users/liyuxiao/Desktop/毕业论文/情感分析训练文本.xlsx')


