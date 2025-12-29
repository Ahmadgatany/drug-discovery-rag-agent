from neo4j import GraphDatabase
from core.config import Config
import logging

class GraphTool:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            Config.NEO4J_URI, 
            auth=(Config.NEO4J_USER, Config.NEO4J_PASSWORD)
        )

        self._initialize_db()

    def _initialize_db(self):
        """Populate the database with initial data if it does not already exist"""
        try:
            self.seed_data(Config.KNOWLEDGE_BASE_SEED)
        except Exception as e:
            logging.error(f"Initial seeding failed: {e}")

    def close(self):
        self.driver.close()

    def seed_data(self, data_list):
        query = """
        MERGE (d:Drug {name: toLower($drug)})
        MERGE (g:Gene {name: toLower($gene)})
        MERGE (dis:Disease {name: toLower($treats)})
        MERGE (d)-[:TARGETS {mechanism: $mechanism}]->(g)
        MERGE (d)-[:TREATS]->(dis)
        SET d.side_effect = $side_effect
        """
        with self.driver.session() as session:
            for item in data_list:
                session.run(query, **item)
        print("[*] Neo4j Graph seeded/verified successfully!")

    def query(self, entity_name):
        """
        Smart search: searches for the entity whether it is a drug, gene, or disease,
        and uses partial matching (CONTAINS) to avoid exact match issues
        """

        if not entity_name or len(entity_name) < 2:
            return "No entity provided for graph search."

        # Advanced Cypher query that searches in all directions and for any type of node
        cypher_query = """
        MATCH (n) 
        WHERE toLower(n.name) CONTAINS toLower($name)
        MATCH (n)-[r]-(t)
        RETURN n.name as source, labels(n)[0] as s_type, 
               type(r) as relation, 
               t.name as target, labels(t)[0] as t_type
        LIMIT 15
        """
        
        try:
            with self.driver.session() as session:
                # Use execute_read as a best practice for operations that do not modify data
                result = session.execute_read(lambda tx: tx.run(cypher_query, name=entity_name).data())
                
                if not result:
                    return f"No structured relations found for '{entity_name}' in Graph."
                
                formatted_results = []
                for row in result:
                    res = f"- {row['source']} ({row['s_type']}) {row['relation']} {row['target']} ({row['t_type']})"
                    formatted_results.append(res)
                
                return "\n".join(formatted_results)
                
        except Exception as e:
            return f"Graph Search Error: The database might be sleeping or credentials incorrect."