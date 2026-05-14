from __future__ import annotations

import ast
import re


def extract_list_and_asking_part(response):
    entities_and_relations_pattern = r"\*\*Entities and Relations\*\*:\s*(\[[^\]]*\])"
    asking_information_pattern = r"\*\*Asking information\*\*:\s*(\[[^\]]*\])"

    entities_and_relations_match = re.findall(entities_and_relations_pattern, response)
    asking_information_match = re.findall(asking_information_pattern, response)

    entities_and_relations = ast.literal_eval(entities_and_relations_match[0]) if entities_and_relations_match else []
    asking_information = ast.literal_eval(asking_information_match[0]) if asking_information_match else []

    return asking_information, entities_and_relations
