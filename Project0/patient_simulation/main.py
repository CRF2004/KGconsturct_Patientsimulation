import pandas as pd

import llm_call as llm
import dialog2
import embedding
import neo4j_access as na
from llm_prompt import prompt
from process_output import extract_list_and_asking_part
from query import query
import dialog2

"""
    索引：：
    提取case图为三元组和实体列表 -> type+name  :embedding -> embedding-id存储
    检索::
    embedding-id 相似度检索 -> top2查询2跳子图 -> prompt给llm生成回答。
"""

# 提取case图为病人描述、三元组[id,relationship,id]和实体字典{id:{'name': 'pus sample','labels':['Sample']}}（文件在entities.txt）
description, triples, entities = query()
print("extract completed")

entities_emb = embedding.convert_to_embedding(entities)

model_path = '/mnt/diskb5/LLM/Qwen/qwen/Qwen2.5_7B-instruct'
tokenizer, model = llm.load_model(model_path)

chat_history = []

while True:
    
    text = input("User: ")
    
    if text == "exit":
        break
    
    ######### 处理用户输入，得到相关实体 ##########
    response = llm.chat_qwen("cuda", tokenizer, model, prompt.triple_prompt.format(query=text)) 
    
    # entities_and_relations 列表, asking_information列表
    asking_information, entities_and_relations = extract_list_and_asking_part(response)
    print(f"u r asking: {asking_information}")
    
    asking_information, entities_and_relations = embedding.convert_to_embedding(asking_information, entities_and_relations)

        #entities_and_relations还没写匹配, 貌似不用

    
    best_match = embedding.match_result(asking_information, entities_emb)
    print(f"match: {best_match}")
    
    relationships = []
    patient_description = ""
    for id in best_match:
        print(f"match entities {entities[id]}")
        for triplet in triples:
            if id == triplet[2]:
                patient_description += f"is {triplet[1]} {entities[id]['name']} {entities[id]['label']} \n"
                
    
    ######### 生成模型回复 #########
    content = prompt.role_prompt.format(description=patient_description)
    system_message = {"role": "system", 
                      "content": content}
    
    response, chat_history = dialog2.chat_qwen("cuda", tokenizer, model, text, system_message, chat_history)
    print(f"SP: {response}")


















    
    
    
    
    
    
    
    
    
    
