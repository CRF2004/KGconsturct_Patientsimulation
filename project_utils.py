from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency for local setup
    load_dotenv = None

ROOT = Path(__file__).resolve().parent
if load_dotenv is not None:
    load_dotenv(ROOT / ".env")
    load_dotenv(ROOT / ".." / ".env")


@dataclass(frozen=True)
class Neo4jConfig:
    uri: str
    user: str
    password: str


DEFAULT_MODEL_PATH = os.getenv(
    "MODEL_PATH",
    "/path/to/your/local/Qwen2.5_7B-instruct",
)
DEFAULT_MODEL_DEVICE = os.getenv("MODEL_DEVICE", "cuda")
DEFAULT_VISIBLE_DEVICES = os.getenv("CUDA_VISIBLE_DEVICES")


def get_model_path() -> str:
    return os.getenv("MODEL_PATH", DEFAULT_MODEL_PATH)


def get_model_device() -> str:
    return os.getenv("MODEL_DEVICE", DEFAULT_MODEL_DEVICE)


def get_visible_devices() -> str | None:
    return os.getenv("CUDA_VISIBLE_DEVICES", DEFAULT_VISIBLE_DEVICES)


def get_neo4j_config() -> Neo4jConfig:
    password = os.getenv("NEO4J_PASSWORD", "")
    if not password:
        raise RuntimeError("NEO4J_PASSWORD is required. Set it in .env or environment variables.")

    return Neo4jConfig(
        uri=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        user=os.getenv("NEO4J_USER", "neo4j"),
        password=password,
    )
