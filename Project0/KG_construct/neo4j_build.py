from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from py2neo import Graph, Node, Relationship

from project_utils import get_neo4j_config
import read_and_write as rw


def connect_to_neo4j():
    cfg = get_neo4j_config()
    graph = Graph(cfg.uri, auth=(cfg.user, cfg.password))
    return graph


def add_nodes(graph, ner_output, entity_nodes, labels):
    """
    创建实体节点
    返回节点字典
    """
    new_labels = set()
    for entity in ner_output:
        if entity["name"] not in entity_nodes.keys():
            node = Node(entity["label"], case=4, name=entity["name"], label=entity["label"], description=entity["description"])
            entity_nodes[entity["name"]] = node
            if entity["label"] not in labels:
                new_labels.add(entity["label"])
    if new_labels:
        print(f"New labels:{str(new_labels)}")
        labels = labels.union(new_labels)
        rw.write_labels(list(new_labels))

    return entity_nodes, labels


def build_graph(graph, entity_nodes, relationships):
    tx = graph.begin()
    try:
        print("Starting to create relationships...")
        for i, relationship in enumerate(relationships, 1):
            source_name = relationship["source"]
            target_name = relationship["target"]
            relationship_description = relationship["relationship_description"]
            relationship_label = relationship["relationship_label"]
            relationship_strength = relationship["relationship_strength"]

            source_node = entity_nodes.get(source_name)
            target_node = entity_nodes.get(target_name)

            if source_node and target_node:
                rel = Relationship(source_node, relationship_label, target_node, strength=relationship_strength, description=relationship_description)
                tx.create(rel)
                print(f"Created relationship {i}/{len(relationships)}: {source_name} -> {target_name}")
            else:
                print(f"Skipping relationship {i}/{len(relationships)}: Missing node for {source_name} or {target_name}")

        tx.commit()
        print("All relationships committed successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
        tx.rollback()
