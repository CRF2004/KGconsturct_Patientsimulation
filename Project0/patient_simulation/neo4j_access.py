from py2neo import Graph, Node, Relationship

connection_config = {
    "uri": "bolt://localhost:7687",
    "auth": ("neo4j", "neoneo44j")
}
def connect_to_neo4j():
    graph = Graph(connection_config["uri"], auth=connection_config["auth"])
    return graph
    
def add_nodes(graph, ner_output, entity_nodes):
    """
        创建实体节点
        返回节点字典
    """
    # 遍历每个实体，创建对应的节点
    for entity in ner_output:
        if entity["name"] not in entity_nodes.keys():
            node = Node(entity["type"], name=entity["name"], type=entity["type"], description=entity["description"])
            entity_nodes[entity["name"]] = node
    return entity_nodes

def build_graph(graph, entity_nodes, re_output):
    for relationship in re_output:
        source_name = relationship["source"]
        target_name = relationship["target"]
        relationship_description = relationship["relationship_description"]
        relationship_label = relationship["relationship_label"]
        relationship_strength = relationship["relationship_strength"]
        
        # 从 entity_nodes 中获取源节点和目标节点
        source_node = entity_nodes.get(source_name)
        target_node = entity_nodes.get(target_name)
        
        if source_node and target_node:
            # 创建关系
            rel = Relationship(source_node, relationship_label, target_node, strength=relationship_strength, description=relationship_description)
            graph.create(rel)