from __future__ import annotations

import os
import pickle
from pathlib import Path

import numpy as np

from embedding_call import Embedding

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_VEC_PATH = Path(os.getenv("EMBEDDING_VEC_PATH", BASE_DIR / "wiki-news-300d-1M-subword.vec"))
CACHE_PATH = Path(os.getenv("EMBEDDING_CACHE_PATH", BASE_DIR / "word_vectors_cache.pkl"))


def convert_to_embedding(entities1, entities2=None):
    """
    调用即加载词表。
    允许传递字典、列表，允许传一个、两个，将返回与传递相应的embedding，不改变数据类型
    """

    def convert(data):
        data = pickle.loads(pickle.dumps(data))

        if isinstance(data, dict):
            for entity_id, entity_info in data.items():
                entity_info['name'] = embedding.entity_embedding(entity_info['name'])
                entity_info['label'] = embedding.entity_embedding(entity_info['label'])
            return data
        elif isinstance(data, list):
            for i, entity_info in enumerate(data):
                data[i] = embedding.entity_embedding(entity_info)
            return data

    embedding = Embedding()

    if entities2 is not None:
        return convert(entities1), convert(entities2)
    else:
        return convert(entities1)


def match_result(entity_list, entity_dict):
    best_match = []
    for entity in entity_list:
        for entity_id, entity_info in entity_dict.items():
            similarity = max(cosine_similarity(entity_info['name'], entity), cosine_similarity(entity_info['label'], entity))
            if similarity > 0.5:
                best_match.append(entity_id)
    print(best_match)
    return best_match


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)

    return dot_product / (norm_vec1 * norm_vec2)
