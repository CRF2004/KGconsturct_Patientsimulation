from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from py2neo import Graph

from project_utils import get_neo4j_config


def connect_to_neo4j():
    cfg = get_neo4j_config()
    return Graph(cfg.uri, auth=(cfg.user, cfg.password))
