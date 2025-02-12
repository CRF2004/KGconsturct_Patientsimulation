import os
import json

from process_output import convert_to_json, decide_gleaning
from transformers import AutoModelForCausalLM, AutoTokenizer
from prompt.prompt0 import ner_prompt, re_prompt, init_prompt, eval_prompt
import llm_call as llm
import read_and_write as rw
import neo4j_build as nb
import create_chunk


# 加载模型
model_path = '/mnt/diskb5/LLM/Qwen/qwen/Qwen2.5_7B-instruct'
tokenizer, model = llm.load_model(model_path) 
#连接图数据库
try:
    graph = nb.connect_to_neo4j()
except Exception as e:
    print(f"An error occurred: {e}")

print("Load and Connection finished")

labels = rw.read_labels()
entity_nodes = {}
# 处理输入文本
chunk = create_chunk.chunk(text=rw.read_text(),
                     chunk_size=5000,
                     over_lap_size=700)
for i in range(len(chunk)):
    print(f"#####Chunk {i+1}#####")
    text = chunk[i]
    is_extraction_complete = False
    
    while is_extraction_complete == False:
        
        new_entity_nodes = {}
        
        ######################### 实体识别 ##########################  
        print("ner start")
        formatted_entity_name =", ".join(list(entity_nodes.keys()))
        prompt1 = " ".join([init_prompt, ner_prompt.format(entity_name=formatted_entity_name, entity_labels=str(labels), text=text)])
        # 提取实体
        response = llm.chat_qwen("cuda", tokenizer, model, prompt1)
        # 处理输出结果
        ner_output = convert_to_json(response)
        rw.write_entity_as_txt(response)
        
        output_tokens = tokenizer(response, return_tensors="pt")
        output_token_count = output_tokens["input_ids"].shape[1]
        print(f"    输出文本的 token 数: {output_token_count}")
        rw.write_entity(ner_output)

        # 建立节点
        new_entity_nodes, labels = nb.add_nodes(graph, ner_output, entity_nodes, labels)
        entity_nodes.update(new_entity_nodes)
        print("ner finished")
        
        ####################### 关系抽取、建图 #######################
        print("re start")
        # 处理输入文本
        formatted_entity_name = ", ".join([f"{node['name']} ({node['type']})" for node in entity_nodes.values()])
        prompt2 = " ".join([init_prompt, re_prompt.format(entity_name=formatted_entity_name, text=text)])
        # 提取关系
        response = llm.chat_qwen("cuda", tokenizer, model, prompt2)
        #处理输出结果
        re_output = convert_to_json(response)
        rw.write_relation_as_txt(response)
            
        output_token_count = output_tokens["input_ids"].shape[1]
        print(f"    输出文本的 token 数: {output_token_count}")
        rw.write_relation(re_output)
        #######################  评估  ############################
        prompt3 = eval_prompt.format(entity_name=formatted_entity_name, text=text)
        response = llm.chat_qwen("cuda", tokenizer, model, prompt3)
        is_extraction_complete = decide_gleaning(response)
        
        print(f"    entity_nodes_count: {len(entity_nodes)}")
        if is_extraction_complete == False:
            print("is_extraction_complete == False")

    #建图
    nb.build_graph(graph, entity_nodes, re_output)

    print("re and graph-build finished")
