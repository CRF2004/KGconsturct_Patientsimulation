import neo4j_access as na
from py2neo import NodeMatcher
def query():
    try:
        graph = na.connect_to_neo4j()
        print("connected")
    except Exception as e:
        print(f"An error occurred: {e}")
    result = graph.run("""
                    MATCH (p:Person)
                    WHERE id(p) = 64
                    RETURN p.description AS description
                        """)
    description = result.data()[0]['description']
    
    # 获取三元组及其对应的实体
    query = """
    MATCH (p:Person)-[r]->(e)
    WHERE id(p) = 64
    RETURN id(p) AS patient_id, type(r) AS relationship_type, id(e) AS entity_id, e.name AS entity_name, labels(e) AS entity_label
    """
    result = graph.run(query)

    triples = []
    entities = {}
    prompt_triple = []
    for record in result:
        patient_id = record["patient_id"]
        relationship_type = record["relationship_type"]
        entity_id = record["entity_id"]
        entity_name = record["entity_name"]
        entity_label = record["entity_label"][0]

        # 保存三元组
        triples.append((patient_id, relationship_type, entity_id))
        prompt_triple.append(f"{relationship_type} {entity_name} as {entity_label}")

        # 保存实体信息
        entities[entity_id] = {"name": entity_name, "label": entity_label}
        
    return description, triples, entities
"""   
# 打印三元组
print("三元组:")
for triple in triples:
    print(triple)
    
# 打印实体列表
print("\n实体列表:")
for entity_id, entity_info in entities.items():
    print(f"ID: {entity_id}, Name: {entity_info['name']}, Labels: {entity_info['labels']}")
    
"""