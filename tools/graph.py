from neo4j import GraphDatabase
from core.config import Config

class GraphTool:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI, 
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()
        
        
    def seed_data(self, data_list):
        query = """
        MERGE (d:Drug {name: $drug})
        MERGE (g:Gene {name: $gene})
        MERGE (dis:Disease {name: $treats})
        MERGE (d)-[:TARGETS {mechanism: $mechanism}]->(g)
        MERGE (d)-[:TREATS]->(dis)
        SET d.side_effect = $side_effect
        """
        with self.driver.session() as session:
            for item in data_list:
                session.run(query, **item)
        print("[*] Neo4j Graph seeded successfully!")

    def query(self, drug_name):
        cypher_query = """
        MATCH (d:Drug {name: $name})-[r]->(t)
        RETURN d.name as drug, type(r) as relation, t.name as target, labels(t)[0] as type
        LIMIT 10
        """
        try:
            with self.driver.session() as session:
                result = session.run(cypher_query, name=drug_name)
                records = [f"{row['drug']} {row['relation']} {row['target']} ({row['type']})" for row in result]
                return "\n".join(records) if records else "No structured data found in Graph."
        except Exception as e:
            return f"Graph query error: {e}"