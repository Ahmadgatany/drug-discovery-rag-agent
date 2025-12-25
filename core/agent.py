from openai import OpenAI
from core.config import Config

class MedicalAgent:
    def __init__(self, graph_tool, vector_tool, web_tool):
        """
        تهيئة الـ Agent وربطه بالأدوات الثلاثة (Graph, Vector, Web)
        """
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=Config.OPENROUTER_API_KEY,
        )
        # تخزين الأدوات داخل الـ Agent
        self.graph = graph_tool
        self.vector = vector_tool
        self.web = web_tool

    def search(self, query: str):
        """
        المحرك الرئيسي للبحث: يجمع البيانات من المصادر الثلاثة ثم يولد الإجابة
        """
        
        # 1. جمع البيانات من المصادر الثلاثة
        graph_results = self.graph.query(query)
        vector_results = self.vector.search(query)
        web_results = self.web.search(query)

        # 2. تخزين المصادر في قاموس لاستخدامها في واجهة Streamlit
        sources = {
            "graph": graph_results,
            "local_literature": vector_results,
            "web_updates": web_results
        }

        # 3. صياغة السياق (Context) الذي سيُرسل للموديل
        context = f"""
        [STRUCTURED DATA FROM KNOWLEDGE GRAPH]:
        {graph_results}
        
        [SCIENTIFIC LITERATURE FROM PUBMED]:
        {vector_results}
        
        [LATEST WEB UPDATES (2024-2025)]:
        {web_results}
        """

        # 4. طلب الإجابة من نموذج Llama 3.3 عبر OpenRouter
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

        # 5. العودة بالقاموس الكامل (الإجابة + المصادر) ليتوافق مع الواجهة
        return {
            "answer": answer,
            "sources": sources
        }