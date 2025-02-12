import re
import json
import os

def convert_to_json(input_string):
    # 正则表达式匹配 JSON 数据
    json_pattern = re.compile(r'(\[.*\])', re.DOTALL)
    # 使用正则表达式查找符合 JSON 格式的部分
    match = json_pattern.search(input_string)

    if match:
        json_str = match.group(1)
        try:
            # 将找到的 JSON 字符串转换为 Python 对象
            json_data = json.loads(json_str)
            # 打印输出 JSON 对象
            # print(json.dumps(json_data, indent=4))
            return json_data
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
    else:
        print("No valid JSON data found in the input string.")
        return None

def decide_gleaning(input_string):

    # 使用正则表达式匹配 "NO"（不区分大小写）
    is_extraction_complete = not bool(re.fullmatch(r"NO", input_string, flags=re.IGNORECASE))

    return is_extraction_complete