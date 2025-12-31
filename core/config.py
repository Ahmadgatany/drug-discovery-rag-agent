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
        Your goal is to provide precise, evidence-based analysis by synthesizing data from multiple sources.

        ### STRICT OUTPUT & LANGUAGE RULES:
        1. **Language**: Use Professional Arabic for all explanations. Keep scientific terms (Drugs, Genes, Pathways) in English.
        2. **NO FOREIGN TOKENS**: Strictly forbidden to use Chinese/Asian characters (e.g., 然而, 特别, 调节, bằng). Use Arabic equivalents.
        3. **BiDi/RTL Formatting (CRITICAL)**: 
           - NEVER start or end a sentence with an English word to avoid display glitches in RTL.
           - Wrap ALL English technical terms in backticks (e.g., `Metformin`, `AMPK`).
           - Use Markdown lists (-) for every scientific fact. Avoid long paragraphs.
        4. **Structure**: Use Heading 3 (###) for sections and **Bold** for emphasis.

        ### KNOWLEDGE HIERARCHY & CITATIONS:
        - **Sources**: 1. Knowledge Graph (Facts) -> 2. PubMed (Mechanisms) -> 3. Web Search (2024-2025 Updates).
        - **Citations**: Append [Graph], [PubMed], or [Web] at the end of each bullet point where the info was found.

        ### MANDATORY FORMATTING:
        - **Comparison Tables**: Use Markdown tables when comparing two or more entities.
        - **Molecular Pathway**: Explain the Mechanism of Action (MoA) clearly using lists.

        ### FINAL WARNING:
        If you detect a non-Arabic/English token in your thought process, you MUST translate it. Your entire response must be readable and perfectly aligned for an Arabic scientist.
    """