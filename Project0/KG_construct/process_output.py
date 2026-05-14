from __future__ import annotations

import ast
import re


def convert_to_json(input_string):
    json_pattern = re.compile(r'(\[.*\])', re.DOTALL)
    match = json_pattern.search(input_string)

    if match:
        json_str = match.group(1)
        try:
            return ast.literal_eval(json_str)
        except (ValueError, SyntaxError) as e:
            print("Error decoding JSON:", e)
    else:
        print("No valid JSON data found in the input string.")
        return None


def decide_gleaning(input_string):
    is_extraction_complete = not bool(re.fullmatch(r"NO", input_string, flags=re.IGNORECASE))
    return is_extraction_complete
