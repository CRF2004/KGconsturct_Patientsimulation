from __future__ import annotations

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
WHOLE_TEXT_FILE = INPUT_DIR / "whole_text.txt"
LABELS_FILE = OUTPUT_DIR / "labels.json"
ENTITY_JSON = OUTPUT_DIR / "entity.json"
ENTITY_TXT = OUTPUT_DIR / "entity.txt"
RELATION_JSON = OUTPUT_DIR / "relation.json"
RELATION_TXT = OUTPUT_DIR / "relation.txt"
DEFAULT_LABELS = [{"node_labels": []}]


def _ensure_input_dir() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_labels_file() -> None:
    _ensure_output_dir()
    if not LABELS_FILE.exists():
        LABELS_FILE.write_text(json.dumps(DEFAULT_LABELS, indent=4, ensure_ascii=False), encoding="utf-8")


def pdf_write(text):
    _ensure_input_dir()
    WHOLE_TEXT_FILE.write_text(text, encoding="utf-8")


def read_text():
    return WHOLE_TEXT_FILE.read_text(encoding="utf-8")


def read_labels():
    _ensure_labels_file()
    data = json.loads(LABELS_FILE.read_text(encoding="utf-8"))
    return set(data[0].get("node_labels", []))


def write_labels(new_labels):
    _ensure_labels_file()
    data = json.loads(LABELS_FILE.read_text(encoding="utf-8"))
    existing = set(data[0].get("node_labels", []))
    existing.update(new_labels)
    data[0]["node_labels"] = sorted(existing)
    LABELS_FILE.write_text(json.dumps(data, indent=4, ensure_ascii=False), encoding="utf-8")


def write_entity(json_output):
    _ensure_output_dir()
    ENTITY_JSON.write_text(json.dumps(json_output, indent=4, ensure_ascii=False), encoding="utf-8")


def write_entity_as_txt(text):
    _ensure_output_dir()
    ENTITY_TXT.write_text(text, encoding="utf-8")


def write_relation(json_output):
    _ensure_output_dir()
    RELATION_JSON.write_text(json.dumps(json_output, indent=4, ensure_ascii=False), encoding="utf-8")


def write_relation_as_txt(text):
    _ensure_output_dir()
    RELATION_TXT.write_text(text, encoding="utf-8")
