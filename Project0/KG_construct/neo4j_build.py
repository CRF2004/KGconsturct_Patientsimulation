from py2neo import Graph, Node, Relationship
import read_and_write as rw

connection_config = {
    "uri": "bolt://localhost:7687",
    "auth": ("neo4j", "neoneo44j")
}
def connect_to_neo4j():
    graph = Graph(connection_config["uri"], auth=connection_config["auth"])
    return graph
    
def add_nodes(graph, ner_output, entity_nodes, labels):
    """
        创建实体节点
        返回节点字典
    """
    new_labels = set()
    # 遍历每个实体，创建对应的节点
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
    # 开启一个事务
    tx = graph.begin()
    try:
        print("Starting to create relationships...")
        for i, relationship in enumerate(relationships, 1):
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
                # 在事务中创建关系
                tx.create(rel)
                print(f"Created relationship {i}/{len(relationships)}: {source_name} -> {target_name}")
            else:
                print(f"Skipping relationship {i}/{len(relationships)}: Missing node for {source_name} or {target_name}")
        
        # 提交事务
        tx.commit()
        print("All relationships committed successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
        # 回滚事务（如果有）
        tx.rollback()