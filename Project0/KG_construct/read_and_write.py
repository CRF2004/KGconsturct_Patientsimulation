import os
import json

def pdf_write(text):
    with open("./input/whole_text.txt", "w", encoding = "utf-8") as f:
        f.write(text)
def read_text():
    with open("./input/whole_text.txt", "r", encoding = "utf-8") as f:
        text = f.read()
    return text
def read_labels():
    with open("./output/labels.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return set(data[0]["node_labels"])
def write_labels(new_labels):
    with open("./output/labels.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data[0]["node_labels"].extend(new_labels)
    with open("./output/labels.json", "w", encoding="utf-8") as w:
        json.dump(data, w, indent=4, ensure_ascii=False)
def write_entity(json_output):
    with open("./output/entity.json", "w", encoding="utf-8") as w:
        json.dump(json_output, w, indent=4, ensure_ascii=False)
def write_entity_as_txt(text):
    with open(f"./output/entity.txt", "w", encoding="utf-8") as w:
        w.write(text)
def write_relation(json_output):
    with open("./output/relation.json", "w", encoding="utf-8") as w:
        json.dump(json_output, w, indent=4, ensure_ascii=False)
def write_relation_as_txt(text):
    with open(f"./output/relation.txt", "w", encoding="utf-8") as w:
        w.write(text)