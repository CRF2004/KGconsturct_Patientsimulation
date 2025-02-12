from transformers import AutoModel, AutoTokenizer, AutoConfig
import torch
import torch.nn.functional as F

import fasttext
import numpy as np
import io
import pickle
class Embedding():
    def __init__(self):
        # 加载词向量
        self.word_dict = self.load_vectors('./wiki-news-300d-1M-subword.vec')
    def load_vectors(self, fname):
        # 尝试从缓存中加载
        try:
            with open('./word_vectors_cache.pkl', 'rb') as f:
                word_dict = pickle.load(f)
                print("Loaded word vectors from cache.")
                return word_dict
        except:
            print("Cache not found, loading from file...")
            # 如果没有缓存，则从文件中加载
            with open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore') as fin:
                n, d = map(int, fin.readline().split())  # 读取文件头
                word_dict = {}
                for line in fin:
                    tokens = line.rstrip().split(' ')
                    word_dict[tokens[0]] = list(map(float, tokens[1:]))
            
            # 保存到缓存
            with open('./word_vectors_cache.pkl', 'wb') as f:
                pickle.dump(word_dict, f)
                print("Saved word vectors to cache.")
            return word_dict
    def token_embedding(self, word):
        if word in self.word_dict:
            return np.array(self.word_dict[word])
        else:
            print(f"The word {word} is not in the dictionary.")
            # raise Exception(f"The word {word} is not in the dictionary.")
            return np.zeros(300)
    def entity_embedding(self, text):
        tokens = text.split()
        
        token_list = []
        for token in tokens:
            vector = self.token_embedding(token)
            if vector is not None:
                token_list.append(vector)

        if token_list:
                entity_vector = np.mean(token_list, axis=0)  # 沿着 token 维度进行平均池化
                return entity_vector
        else:
            print(f"No valid token embeddings found for entity '{text}'")
            return None


# vec1 = entity_embedding("laboratory Test")
# vec2 = entity_embedding("Blood Chemistry Investigations")
# vec3 = entity_embedding("Difficulty in Breathing")
# print(f"similar {cosine_similarity(vec1, vec2)}")
# print(f"unsimilar {cosine_similarity(vec1, vec3)}")

"""
#def load_model(model_path):
model_path = "./biobert-pytorch-master0/biobert-base-cased-v1.1"
config = AutoConfig.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(
    model_path,
    torch_dtype="auto",
    device_map="auto",
    #device_map={"": "cuda:5"} # 指定模型加载到 GPU 上
    )
#return model, tokenizer

def token_embedding(text):
    inputs = tokenizer(text, return_tensors="pt")   #分词，返回张量

    # 获取 token ids
    token_ids = inputs["input_ids"]
    tokens = tokenizer.convert_ids_to_tokens(token_ids[0])
    print(tokens)
    # 获取模型输出
    with torch.no_grad():
        outputs = model(**inputs)

    last_hidden_state = outputs.last_hidden_state[0, 1:-1, :]   # 获取 token-level 的嵌入（last_hidden_state）
    return last_hidden_state


def entity_embedding(text):
    token_embedding_result = token_embedding(text)
    # 对每个维度进行平均池化，得到实体的向量表示
    entity_embedding = token_embedding_result.mean(dim=0)
    return entity_embedding

entity_embedding_1 = entity_embedding("Cancer")
entity_embedding_2 = entity_embedding("Heart Disease")
cos_sim = F.cosine_similarity(entity_embedding_1, entity_embedding_2, dim=0)
# 转换为余弦距离
cos_distance = 1 - cos_sim

print(f"Cosine Similarity: {cos_sim.item()}")
print(f"Cosine Distance: {cos_distance.item()}")
#########################################################
entity_embedding_1 = entity_embedding("Heart Disease")
entity_embedding_2 = entity_embedding("Alien")
cos_sim = F.cosine_similarity(entity_embedding_1, entity_embedding_2, dim=0)
# 转换为余弦距离
cos_distance = 1 - cos_sim

print(f"Cosine Similarity: {cos_sim.item()}")
print(f"Cosine Distance: {cos_distance.item()}")
"""