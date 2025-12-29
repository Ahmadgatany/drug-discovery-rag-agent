from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from core import Config, MedicalAgent
from tools import GraphTool, VectorTool, PubMedTool, WebSearchTool

app = FastAPI(title="Drug Discovery RAG API")

graph_tool = GraphTool()
vector_tool = VectorTool()
pubmed_tool = PubMedTool()
web_tool = WebSearchTool()


agent = MedicalAgent(graph_tool, vector_tool, web_tool)

@app.on_event("startup")
async def startup_event():
    """
    This function runs automatically when the server starts to populate Neo4j with initial data.
    """

    print("[*] Checking Knowledge Base Seed in Neo4j...")
    try:
        graph_tool.seed_data(Config.KNOWLEDGE_BASE_SEED)
    except Exception as e:
        print(f"[!] Skipping seeding or Neo4j not ready: {e}")

class QueryRequest(BaseModel):
    prompt: str

@app.post("/ask")
async def ask_agent(request: QueryRequest):
    try:
        print(f"\n[*] New Request Received: {request.prompt}")
        
        print("[*] Searching PubMed for latest papers...")
        new_docs = pubmed_tool.search_and_fetch(request.prompt)
        print(f"[*] Found {len(new_docs)} papers.")

        if new_docs:
            print("[*] Updating local Vector Database...")
            vector_tool.add_texts(new_docs)
        
        print("[*] Thinking... Generating comprehensive answer.")
        result = agent.search(request.prompt)
        
      # Note: `result` here is: {"answer": "...", "sources": {"graph": "...", "local_literature": "...", "web_updates": "..."}}

        return result 
        
    except Exception as e:
        print(f"[!] ERROR OCCURRED: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)