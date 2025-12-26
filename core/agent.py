from openai import OpenAI
from core.config import Config

class MedicalAgent:
    def __init__(self, graph_tool, vector_tool, web_tool):
        """
        Initialize the Agent and connect it with the three tools (Graph, Vector, Web)
        """
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=Config.OPENROUTER_API_KEY,
        )
        # Store the tools inside the Agent
        self.graph = graph_tool
        self.vector = vector_tool
        self.web = web_tool

    def search(self, query: str):
        """
        Main search engine: gathers data from the three sources and then generates the answer
        """
        
        graph_results = self.graph.query(query)
        vector_results = self.vector.search(query)
        web_results = self.web.search(query)

        sources = {
            "graph": graph_results,
            "local_literature": vector_results,
            "web_updates": web_results
        }

        context = f"""
        [STRUCTURED DATA FROM KNOWLEDGE GRAPH]:
        {graph_results}
        
        [SCIENTIFIC LITERATURE FROM PUBMED]:
        {vector_results}
        
        [LATEST WEB UPDATES (2024-2025)]:
        {web_results}
        """

        try:
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[
                    {"role": "system", "content": Config.SYSTEM_PROMPT},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"}
                ],
                temperature=Config.TEMPERATURE
            )
            
            answer = response.choices[0].message.content
        except Exception as e:
            answer = f"عذراً، حدث خطأ أثناء توليد الإجابة: {str(e)}"

        return {
            "answer": answer,
            "sources": sources
        }
