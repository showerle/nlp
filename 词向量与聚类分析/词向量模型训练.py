# 词向量模型训练


def model_train(train_file_name, save_model_name):  # model_file_name为训练语料的路径,save_model为保存模型名
    from gensim.models import word2vec
    import gensim
    import logging
    # 模型训练，生成词向量
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    sentences = word2vec.Text8Corpus(train_file_name)  # 加载语料
    # 训练skip-gram模型;
    model = gensim.models.Word2Vec(sentences, vector_size=200, window=10, min_count=1, workers=4, sg=1)
    model.save(save_model_name)
    model.wv.save_word2vec_format(save_model_name + ".bin", binary=True)   # 以二进制类型保存模型以便重用


model_train("/Users/liyuxiao/Desktop/毕业论文/美食评论文本.txt", "美食评论文本.model")

