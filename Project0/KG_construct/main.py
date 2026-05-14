from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from process_output import convert_to_json, decide_gleaning
from prompt.prompt0 import ner_prompt, re_prompt, init_prompt, eval_prompt1, eval_prompt2, gleaning_prompt
import llm_call as llm
import read_and_write as rw
import neo4j_build as nb
import create_chunk
from project_utils import get_model_path


def main():
    model_path = get_model_path()
    tokenizer, model = llm.load_model(model_path)

    try:
        graph = nb.connect_to_neo4j()
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    print("Load and Connection finished")

    labels = rw.read_labels()
    entity_nodes = {}
    chunk = create_chunk.chunk(rw.read_text(), 5000, 700)

    for i, text in enumerate(chunk, start=1):
        print(f"#####Chunk {i}#####")
        is_extraction_complete = False
        attempt = 0

        while not is_extraction_complete:
            print("ner start")
            formatted_entity_name = ", ".join(list(entity_nodes.keys()))
            if attempt == 0:
                prompt1 = " ".join([init_prompt, ner_prompt.format(entity_name=formatted_entity_name, entity_labels=str(labels), text=text)])
            else:
                prompt1 = gleaning_prompt.format(entity_name=str(entity_nodes), entity_labels=str(labels), text=text)

            response = llm.chat_qwen("cuda", tokenizer, model, prompt1)
            ner_output = convert_to_json(response)
            rw.write_entity_as_txt(response)
            if ner_output is None:
                print("NER output could not be parsed; retrying")
                attempt += 1
                if attempt >= 4:
                    break
                continue

            output_tokens = tokenizer(response, return_tensors="pt")
            print(f"    输出文本的 token 数: {output_tokens['input_ids'].shape[1]}")
            rw.write_entity(ner_output)

            new_entity_nodes, labels = nb.add_nodes(graph, ner_output, entity_nodes, labels)
            entity_nodes.update(new_entity_nodes)
            print("ner finished")

            prompt3 = eval_prompt1.format(entity_name=formatted_entity_name, text=text)
            response = llm.chat_qwen("cuda", tokenizer, model, prompt3)
            is_extraction_complete = decide_gleaning(response)
            print(f"    entity_nodes_count: {len(entity_nodes)}")
            if not is_extraction_complete:
                print("is_extraction_complete == False")
                attempt += 1
                if attempt >= 4:
                    break

    print("//////re//////")
    relationships = []
    formatted_entity_name = ", ".join([f"{node['name']} ({node['type']})" for node in entity_nodes.values()])

    for i, text in enumerate(chunk, start=1):
        print(f"#####Chunk {i}#####")
        is_extraction_complete = False
        attempt = 0
        new_relationships = []
        prompt2 = " ".join([init_prompt, re_prompt.format(entity_name=formatted_entity_name, text=text)])

        while not is_extraction_complete:
            print("re start")
            response = llm.chat_qwen("cuda", tokenizer, model, prompt2)
            re_output = convert_to_json(response)
            rw.write_relation_as_txt(response)
            if re_output is not None:
                new_relationships.extend(re_output)
                rw.write_relation(re_output)

            prompt3 = eval_prompt2.format(relationships=relationships, entity_name=formatted_entity_name, text=text)
            response = llm.chat_qwen("cuda", tokenizer, model, prompt3)
            is_extraction_complete = decide_gleaning(response)
            if not is_extraction_complete:
                print("is_extraction_complete == False")
                attempt += 1
                if attempt >= 4:
                    break
            print("re finished")

        relationships.extend(new_relationships)
        print(f"    relationships_count: {len(relationships)}")

    nb.build_graph(graph, entity_nodes, relationships)
    print("graph-build finished")


if __name__ == "__main__":
    main()
