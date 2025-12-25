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

    ### LANGUAGE & OUTPUT POLICY (STRICT):
    - Primary Language: PROFESSIONAL ARABIC.
    - Technical Terms: English (e.g., SGLT2, Dipeptidyl peptidase-4).
    - NO LANGUAGE MIXING: Never use French, Vietnamese, or any other languages.

    ### KNOWLEDGE HIERARCHY:
    1. Structured Graph: Verified facts (Drug-Target-Disease).
    2. Local Literature (PubMed): Deep clinical outcomes and mechanisms.
    3. Web Search: Real-time updates (2024-2025 news).

    ### RESPONSE FORMAT:
    - Use Comparison Tables for drugs.
    - Use Bold Headings for sections.
    - Cite [PubMed] and [Web] clearly.
    """