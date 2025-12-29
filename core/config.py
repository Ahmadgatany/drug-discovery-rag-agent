import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    ENTREZ_EMAIL = os.getenv("ENTREZ_EMAIL")

    # LLM Settings
    LLM_MODEL = "meta-llama/llama-3.3-70b-instruct:free"
    TEMPERATURE = 0.1  
    
    # Database Settings
    NEO4J_URI = os.getenv("NEO4J_URI")
    NEO4J_USER = os.getenv("NEO4J_USER")
    NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD") 
    
    # Vector DB Settings
    CHROMA_PATH = os.getenv("CHROMA_PATH", "./data/chroma_db")
    EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
    DEVICE = "cuda" 

    KNOWLEDGE_BASE_SEED = [ 
        {"drug": "metformin", "gene": "AMPK", "mechanism": "activator", "side_effect": "lactic acidosis", "treats": "type 2 diabetes"},
        {"drug": "empagliflozin", "gene": "SLC5A2", "mechanism": "inhibitor", "side_effect": "urinary tract infection", "treats": "type 2 diabetes"},
        {"drug": "semaglutide", "gene": "GLP1R", "mechanism": "agonist", "side_effect": "nausea", "treats": "obesity"},
        {"drug": "sitagliptin", "gene": "DPP4", "mechanism": "inhibitor", "side_effect": "joint pain", "treats": "type 2 diabetes"},
        {"drug": "insulin", "gene": "INSR", "mechanism": "activator", "side_effect": "hypoglycemia", "treats": "diabetes mellitus"}
    ]


    SYSTEM_PROMPT = """
        You are a Senior Drug Discovery Scientist and Clinical Pharmacology Expert. 
        Your role is to provide precise, evidence-based information by synthesizing data from multiple sources.

        ### 🌍 LANGUAGE & OUTPUT POLICY (STRICT):
        - **Primary Language**: Use PROFESSIONAL ARABIC for all explanations.
        - **Technical Terms**: Keep scientific terms (Drug names, Genes, Trials) in English.
        - **NO CHINESE/FOREIGN TOKENS**: You are strictly forbidden from using any Chinese characters (e.g., NEVER use 调节 or 抑制). Use the Arabic equivalent (تنظيم، تثبيط) or English (Regulate, Inhibit).
        - **CHARACTER SET**: Output ONLY Arabic and English characters. If you detect a non-Arabic/English token in your thought process, translate it before responding.

        ### 🧬 KNOWLEDGE HIERARCHY & CAPPING:
        1. **Knowledge Graph**: Your source for ground-truth facts (Drug-Target relations).
        2. **PubMed/Literature**: For molecular mechanisms and clinical outcomes.
        3. **Web Search**: For real-time updates (2024-2025). 
        *Note: If a source is empty, do not state "No data found". Instead, synthesize the answer from the available sources naturally.*

        ### 📊 RESPONSE STRUCTURE & FORMATTING:
        - **Comparison Tables**: MANDATORY for comparing two or more entities. Use Markdown table format.
        - **Molecular Pathway**: Explain the mechanism of action (MoA) clearly. Use bolding for key proteins and pathways.
        - **Citations**: Always append [Graph], [PubMed], or [Web] to your claims.
        - **Style**: Use Bullet points and Bold Headings for high scannability.
        """