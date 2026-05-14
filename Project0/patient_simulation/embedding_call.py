from __future__ import annotations

import os
from pathlib import Path

import numpy as np

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_VEC_PATH = Path(os.getenv("EMBEDDING_VEC_PATH", BASE_DIR / "wiki-news-300d-1M-subword.vec"))
CACHE_PATH = Path(os.getenv("EMBEDDING_CACHE_PATH", BASE_DIR / "word_vectors_cache.pkl"))


class Embedding:
    def __init__(self):
        self.word_dict = self.load_vectors(DEFAULT_VEC_PATH)

    def load_vectors(self, fname):
        try:
            with open(CACHE_PATH, 'rb') as f:
                word_dict = __import__("pickle").load(f)
                print("Loaded word vectors from cache.")
                return word_dict
        except Exception:
            print("Cache not found, loading from file...")
            with open(fname, 'r', encoding='utf-8', newline='\n', errors='ignore') as fin:
                _n, _d = map(int, fin.readline().split())
                word_dict = {}
                for line in fin:
                    tokens = line.rstrip().split(' ')
                    word_dict[tokens[0]] = list(map(float, tokens[1:]))
            with open(CACHE_PATH, 'wb') as f:
                __import__("pickle").dump(word_dict, f)
                print("Saved word vectors to cache.")
            return word_dict

    def token_embedding(self, word):
        if word in self.word_dict:
            return np.array(self.word_dict[word])
        print(f"The word {word} is not in the dictionary.")
        return np.zeros(300)

    def entity_embedding(self, text):
        tokens = text.split()
        token_list = []
        for token in tokens:
            vector = self.token_embedding(token)
            if vector is not None:
                token_list.append(vector)

        if token_list:
            return np.mean(token_list, axis=0)
        print(f"No valid token embeddings found for entity '{text}'")
        return None
