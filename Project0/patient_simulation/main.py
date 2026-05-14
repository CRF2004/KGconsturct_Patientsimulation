from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

import llm_call as llm
import dialog2
import embedding
from llm_prompt import prompt
from process_output import extract_list_and_asking_part
from query import query
from project_utils import get_model_path

"""
索引：：
提取case图为三元组和实体列表 -> type+name  :embedding -> embedding-id存储
检索::
embedding-id 相似度检索 -> top2查询2跳子图 -> prompt给llm生成回答。
"""


def main():
    description, triples, entities = query()
    print("extract completed")

    entities_emb = embedding.convert_to_embedding(entities)

    model_path = get_model_path()
    tokenizer, model = llm.load_model(model_path)

    chat_history = []

    while True:
        text = input("User: ")

        if text == "exit":
            break

        response = llm.chat_qwen("cuda", tokenizer, model, prompt.triple_prompt.format(query=text))
        asking_information, entities_and_relations = extract_list_and_asking_part(response)
        print(f"u r asking: {asking_information}")

        asking_information, entities_and_relations = embedding.convert_to_embedding(asking_information, entities_and_relations)
        best_match = embedding.match_result(asking_information, entities_emb)
        print(f"match: {best_match}")

        relationships = []
        patient_description = ""
        for id in best_match:
            print(f"match entities {entities[id]}")
            for triplet in triples:
                if id == triplet[2]:
                    patient_description += f"is {triplet[1]} {entities[id]['name']} {entities[id]['label']} \n"

        content = prompt.role_prompt.format(description=patient_description)
        system_message = {"role": "system", "content": content}

        response, chat_history = dialog2.chat_qwen("cuda", tokenizer, model, text, system_message, chat_history)
        print(f"SP: {response}")


if __name__ == "__main__":
    main()
