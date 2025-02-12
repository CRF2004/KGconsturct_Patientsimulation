import llm_call as llm
import create_chunk
import json
    
prompt1 = """
You are a medical knowledge extraction expert. 
Given the following patient case report text, extract the relevant entity labels
(such as "Symptom", "Laboratory Test") and relationship types (such as "Has_symptom", "Cause_of").
You've recognize the following labels and types:
{labels}
Keep the labels and types minimal.
**Do not add new labels and types unless necessary.**
**do not repeat labels and types that have already been identified and added to the label and type set.**
Example output1:
{{
    'node_labels': {{"Symptom", "Laboratory Test"}},
    'relationship_types': {{"Has_symptom", "Cause_of"}}
}}
Example output2:
{{
    'node_labes': {{"Diagnosis", "Medication"}},
    'relationship_types': {{"Allergic_to", "Has_treatment"}}
}}
Text: {text}
"""
with open("./output/labels.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    
labels = data[0]["node_labels"]

# 加载模型
model_path = '/mnt/diskb5/LLM/Qwen/qwen/Qwen2.5_7B-instruct'
tokenizer, model = llm.load_model(model_path) 

print("Load finished")

entity_labels = {}
relationship_labels = {}
chunk = create_chunk.chunk(4)
for i in {3}:#range(len(chunk)):
    text = chunk[i]

    # 提取实体
    response = llm.chat_qwen("cuda", tokenizer, model, prompt1.format(text=text,labels=str(labels)))
    print(response)
    with open("labels.txt", "a", encoding="utf-8") as f:
        f.write(response)