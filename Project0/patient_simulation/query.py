from __future__ import annotations

import os

import neo4j_access as na


PATIENT_NODE_ID = int(os.getenv("PATIENT_NODE_ID", "64"))


def query():
    try:
        graph = na.connect_to_neo4j()
        print("connected")
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Neo4j: {e}") from e

    result = graph.run(
        """
        MATCH (p:Person)
        WHERE id(p) = $patient_id
        RETURN p.description AS description
        """,
        patient_id=PATIENT_NODE_ID,
    )
    description = result.data()[0]["description"]

    query_text = """
    MATCH (p:Person)-[r]->(e)
    WHERE id(p) = $patient_id
    RETURN id(p) AS patient_id, type(r) AS relationship_type, id(e) AS entity_id, e.name AS entity_name, labels(e) AS entity_label
    """
    result = graph.run(query_text, patient_id=PATIENT_NODE_ID)

    triples = []
    entities = {}
    prompt_triple = []
    for record in result:
        patient_id = record["patient_id"]
        relationship_type = record["relationship_type"]
        entity_id = record["entity_id"]
        entity_name = record["entity_name"]
        entity_label = record["entity_label"][0]

        triples.append((patient_id, relationship_type, entity_id))
        prompt_triple.append(f"{relationship_type} {entity_name} as {entity_label}")
        entities[entity_id] = {"name": entity_name, "label": entity_label}

    return description, triples, entities
