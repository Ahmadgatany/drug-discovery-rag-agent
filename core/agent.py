from openai import OpenAI
from core.config import Config
import re

class MedicalAgent:
    def __init__(self, graph_tool, vector_tool, web_tool):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=Config.OPENROUTER_API_KEY,
        )
        self.graph = graph_tool
        self.vector = vector_tool
        self.web = web_tool

    def _clean_text(self, text: str) -> str:
        """
        Removes any characters that are not Arabic, English, or basic mathematical symbols.
        Used to clean outputs from unusual Chinese or other Asian characters.
        """
        pattern = re.compile(r'[^\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFFa-zA-Z0-9\s.,!?:;()\[\]\-_*#%/\"\'\n]')
        cleaned_text = pattern.sub('', text)
        
        return cleaned_text.strip()

    def _extract_entities(self, query: str):
        extraction_prompt = f"""
        Extract ONLY the medical entities (Drug names, Genes, or Diseases) from the following text.
        Return them as a comma-separated list in English.
        Text: "{query}"
        Example Output: Metformin, Type 2 Diabetes
        Entities:"""
        
        try:
            response = self.client.chat.completions.create(
                model=Config.LLM_MODEL,
                messages=[{"role": "user", "content": extraction_prompt}],
                max_tokens=50,
                temperature=0 
            )
            entities_text = response.choices[0].message.content.strip()
            entities = [e.strip() for e in entities_text.split(",") if e.strip()]
            return entities
        except:
            return []

    def search(self, query: str):
        entities = self._extract_entities(query)

        graph_context_list = []
        if entities:
            for entity in entities:
                res = self.graph.query(entity)
                if "No structured" not in res:
                    graph_context_list.append(res)
        
        graph_results = "\n".join(graph_context_list) if graph_context_list else "No structured data found in Graph."

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
                temperature=Config.TEMPERATURE,
                top_p=0.9,             
                frequency_penalty=0.3 
            )
            raw_answer = response.choices[0].message.content
            
            # تطبيق الفلتر لتنظيف الإجابة من الكلمات الصينية أو الغريبة
            answer = self._clean_text(raw_answer)

        except Exception as e:
            answer = f"عذراً، حدث خطأ أثناء توليد الإجابة: {str(e)}"

        return {
            "answer": answer,
            "sources": sources
        }