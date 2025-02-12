import re

def extract_list_and_asking_part(response):
    # 定义正则表达式模式来提取 Entities and Relations 部分
    entities_and_relations_pattern = r"\*\*Entities and Relations\*\*:\s*(\[[^\]]*\])"
    # 定义正则表达式模式来提取 Asking information 部分
    asking_information_pattern = r"\*\*Asking information\*\*:\s*(\[[^\]]*\])"

    # 使用 re.findall 提取两个部分的内容
    entities_and_relations_match = re.findall(entities_and_relations_pattern, response)
    asking_information_match = re.findall(asking_information_pattern, response)

    # 如果找到匹配项，将其转换为列表
    entities_and_relations = eval(entities_and_relations_match[0]) if entities_and_relations_match else []
    asking_information = eval(asking_information_match[0]) if asking_information_match else []

    return asking_information, entities_and_relations
