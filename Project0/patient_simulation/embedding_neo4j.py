import neo4j_access as na
try:
    graph = na.connect_to_neo4j()
    print("connected")
except Exception as e:
    print(f"An error occurred: {e}")

cypher = """
    MATCH (n) 
    WHERE ID(n) IN range(62,109)
    SET n.embedding = []
"""
cypher = """
    CREATE VECTOR INDEX node_vec_index IF NOT EXISTS
    FOR (m:)
    ON m.embedding
    OPTIONS { indexConfig: {
    `vector.dimensions`: 300,
    `vector.similarity_function`: 'cosine'
    }
    }
"""
graph.run(cypher)
print("Completed")
    
