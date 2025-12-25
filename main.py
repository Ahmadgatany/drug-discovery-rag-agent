# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from core.agent import MedicalAgent
# from tools.graph import GraphTool
# from tools.vector_db import VectorTool
# from tools.pubmed import PubMedTool
# from tools.web_search import WebSearchTool

# app = FastAPI(title="Drug Discovery RAG API")

# # تهيئة الأدوات والـ Agent
# graph_tool = GraphTool()
# vector_tool = VectorTool()
# pubmed_tool = PubMedTool()
# web_tool = WebSearchTool()

# agent = MedicalAgent(graph_tool, vector_tool, web_tool)

# class QueryRequest(BaseModel):
#     prompt: str



# @app.post("/ask")
# async def ask_agent(request: QueryRequest):
#     try:
#         # طباعة السؤال للتأكد من وصوله
#         print(f"[*] Received query: {request.prompt}")
        
#         # 1. تحديث PubMed
#         new_docs = pubmed_tool.search_and_fetch(request.prompt)
#         print(f"[*] Found {len(new_docs)} papers on PubMed")
        
#         # 2. إضافة للـ Vector Store
#         vector_tool.add_texts(new_docs)
        
#         # 3. استدعاء الـ Agent
#         answer = agent.search(request.prompt)
#         return {"answer": answer}
#     except Exception as e:
#         # هذا السطر سيطبع لك الخطأ بالتفصيل في الـ Terminal
#         print(f"[!] ERROR OCCURRED: {str(e)}")
#         raise HTTPException(status_code=500, detail=str(e))

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
# =========================================================
    
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core import Config, MedicalAgent
from tools import GraphTool, VectorTool, PubMedTool, WebSearchTool

app = FastAPI(title="Drug Discovery RAG API")

# 1. تهيئة الأدوات
graph_tool = GraphTool()
vector_tool = VectorTool()
pubmed_tool = PubMedTool()
web_tool = WebSearchTool()

# 2. تهيئة الـ Agent
agent = MedicalAgent(graph_tool, vector_tool, web_tool)

# --- تحسين: تغذية قاعدة البيانات عند تشغيل السيرفر ---
@app.on_event("startup")
async def startup_event():
    """
    هذه الدالة تعمل تلقائياً عند تشغيل السيرفر لتغذية Neo4j بالبيانات الأولية
    """
    print("[*] Checking Knowledge Base Seed in Neo4j...")
    try:
        # استدعاء دالة seed_data التي أضفناها في ملف graph.py
        graph_tool.seed_data(Config.KNOWLEDGE_BASE_SEED)
    except Exception as e:
        print(f"[!] Skipping seeding or Neo4j not ready: {e}")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        print(f"\n[*] New Request Received: {request.prompt}")
        
        # 1. تحديث PubMed (جلب أبحاث جديدة بناءً على السؤال)
        print("[*] Searching PubMed for latest papers...")
        new_docs = pubmed_tool.search_and_fetch(request.prompt)
        print(f"[*] Found {len(new_docs)} papers.")
        
        # 2. إضافة الأبحاث للـ Vector Store (ChromaDB)
        if new_docs:
            print("[*] Updating local Vector Database...")
            vector_tool.add_texts(new_docs)
        
        # 3. استدعاء الـ Agent (الذي يعيد الآن قاموساً يحتوي على answer و sources)
        print("[*] Thinking... Generating comprehensive answer.")
        result = agent.search(request.prompt)
        
        # ملاحظة: result هنا هو: {"answer": "...", "sources": {"graph": "...", "local_literature": "...", "web_updates": "..."}}
        return result 
        
    except Exception as e:
        print(f"[!] ERROR OCCURRED: {str(e)}")
        # إرسال تفاصيل الخطأ للـ Frontend لعرضها للمستخدم
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # تشغيل السيرفر
    uvicorn.run(app, host="127.0.0.1", port=8000)