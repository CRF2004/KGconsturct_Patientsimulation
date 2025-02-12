from embedding_call import Embedding
import numpy as np
import copy
def convert_to_embedding(entities1, entities2=None):
    """
        调用即加载词表。
        允许传递字典、列表，允许传一个、两个，将返回与传递相应的embedding，不改变数据类型
    """
    def convert(data):
        # 对传入的数据进行深拷贝，避免修改原始数据
        data = copy.deepcopy(data)
        
        if isinstance(data, dict):
            for entity_id, entity_info in data.items():
                entity_info['name'] = embedding.entity_embedding(entity_info['name'])
                entity_info['label'] = embedding.entity_embedding(entity_info['label'])
            return data
        elif isinstance(data, list):
            for i, entity_info in enumerate(data):
                data[i] = embedding.entity_embedding(entity_info)
            return data
        
    embedding = Embedding()
    
    if entities2 is not None:
        return convert(entities1), convert(entities2)
    else:
        return convert(entities1)


def match_result(entity_list, entity_dict):
    best_match = []
    for entity in entity_list:
        for entity_id, entity_info in entity_dict.items():
            
            similarity = max(cosine_similarity(entity_info['name'], entity),cosine_similarity(entity_info['label'], entity))
            if similarity > 0.5:
                best_match.append(entity_id)
            # print(similarity) 
    print(best_match)
    return best_match
def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)    # 计算点积
    norm_vec1 = np.linalg.norm(vec1)    # 计算两个向量的模长
    norm_vec2 = np.linalg.norm(vec2)
    
    return dot_product / (norm_vec1 * norm_vec2)     # 计算并返回余弦相似度
"""          
entity_dict = {71: {'name': 'Middle Finger Swelling', 'label': 'Physical Finding'}, 
               90: {'name': 'Hydrocortisone', 'label': 'Pharmacological Agent'}, 
               89: {'name': 'Pantoprazole', 'label': 'Pharmacological Agent'}, 
               88: {'name': 'Dextrose Normal Saline', 'label': 'IV Fluid'}}
entity_list = ['drug']

entity_dict_emb = convert_to_embedding(entity_dict)
entity_list_emb = convert_to_embedding(entity_list)
    
best_match = match_result(entity_list_emb, entity_dict_emb)
print("best_match:")
print(best_match)
"""


