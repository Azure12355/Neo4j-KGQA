# coding:utf-8
import os
import pickle
import time

from sentence_transformers import SentenceTransformer, util

os.environ['CURL_CA_BUNDLE'] = ''
os.environ['REQUESTS_CA_BUNDLE'] = ''


# 如果没有GPU可用，给出警告提示
# if not torch.cuda.is_available():
#     print("Warning: No GPU detected. Processing will be slow. Please add a GPU to this notebook")

class SBert:
    def __init__(self):
        self.model_name = 'quora-distilbert-multilingual'

        self.model = SentenceTransformer(self.model_name)  # 加载SBERT模型
        self.corpus_sentences = set()  # 初始化语料库句子集合
        self.corpus_embeddings = []  # 初始化语料库句子向量列表

    # 从文件中加载症状数据集，为每个症状生成对应的句子向量。首先从文件中获取所有唯一的句子，然后使用SBERT模型对这些句子进行编码，生成语料库句子向量并存储到文件中。
    def store_embedding(self):
        dataset_path = "/data/output/disease_symptom_ac.tsv"
        max_corpus_size = 100000
        # 从文件中获取所有唯一的句子
        with open(dataset_path, encoding='utf8') as fIn:
            for row in fIn:
                self.corpus_sentences.add(row.strip())  # 把疾病名称和疾病症状拼接起来
                if len(self.corpus_sentences) >= max_corpus_size:
                    break
        self.corpus_sentences = list(self.corpus_sentences)
        print("Encode the corpus. This might take a while")
        self.corpus_embeddings = self.model.encode(self.corpus_sentences, show_progress_bar=True,
                                                   convert_to_tensor=True)  # 生成语料库句子向量并存储到文件中

        print("Corpus loaded with {} sentences / embeddings".format(len(self.corpus_sentences)))
        # 将句子和向量保存到文件中
        with open('symptom_embedding/embeddings.pkl', "wb") as fOut:
            pickle.dump({'sentences': self.corpus_sentences, 'embeddings': self.corpus_embeddings}, fOut,
                        protocol=pickle.HIGHEST_PROTOCOL)

    # 从文件中加载句子和向量，用于后续的语义匹配搜索。
    def load_embedding(self):
        # 从文件中加载句子和向量
        with open(
                'D:\\Code\GitHubProject\\medical_knowledge_graph_app-master\\med_kg\\el_model\\embedding\\disease_embeddings.pkl',
                "rb") as fIn:
            stored_data = pickle.load(fIn)
            self.corpus_sentences = stored_data['sentences']
            self.corpus_embeddings = stored_data['embeddings']

    def search(self, inp_question):
        start_time = time.time()
        question_embedding = self.model.encode(inp_question, convert_to_tensor=True)
        hits = util.semantic_search(question_embedding, self.corpus_embeddings)
        end_time = time.time()
        print('test-hits', hits)
        hits = hits[0]  # 获取第一个查询的匹配结果

        top_1_symptom = self.corpus_sentences[hits[0]['corpus_id']][:-6]
        print('找到了语义最相似的症状：' + top_1_symptom)
        return top_1_symptom


# 主程序入口
if __name__ == '__main__':
    # 存储
    # model = SBert()
    # model.store_embedding()

    # 导出
    model = SBert()
    model.load_embedding()
    while 1:
        question = input('用户:')  # 用户输入问题句子
        top1_symptom = model.search(question)  # 进行语义匹配搜索

    # 语义匹配例子：
    # 用户: 皮肤痕痒，红肿是什么毛病？
    # 找到了语义最相似的症状：皮肤弥漫性红肿
    #
    # 用户: 眼睛干涩是什么毛病？
    # 找到了语义最相似的症状：眼干
    #
    # 用户: 嘴唇旁边干裂是什么毛病？
    # 找到了语义最相似的症状：唇干裂
