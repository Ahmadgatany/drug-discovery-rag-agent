# 🧬 Drug Discovery AI Explorer: Advanced Graph-RAG System

An expert-grade AI system designed for pharmaceutical researchers. It utilizes **Graph-Augmented Retrieval (Graph-RAG)** to provide precise, evidence-based analysis of drug-target interactions, molecular pathways, and clinical trial updates.

---

## 🌟 Why This Project?

Traditional RAG systems often suffer from "context fragmentation" in the medical field. Biologically, data is not just text—it is a network of connections (Drug  Target  Disease).

**Our Solution:**

* **Structured Truth:** Uses Neo4j to prevent "AI hallucinations" by tracing verified biological paths.
* **Scientific Grounding:** Cross-references every claim against PubMed literature and real-time Web Search (2024-2025).
* **Reasoning Capability:** Leverages Llama 3.3 to synthesize complex multi-source data into a professional Arabic/English report.

---

## 📸 System in Action

Stage 1: Query & Search,Stage 2: Synthesized Analysis
"<img src=""assets/1.png"" width=""400"">","<img src=""assets/2.png"" width=""400"">"
Agent orchestrating multi-source retrieval.,Final clinical report with grounded citations.
---

## 🏗️ Project Architecture

```text
DrugDiscoveryRAG/
├── .env                  # API Keys & DB Credentials
├── .gitignore            # Excluded files
├── README.md             # Documentation
├── requirements.txt      # Dependencies
├── main.py               # FastAPI Backend (Orchestration)
├── app.py                # Streamlit Frontend (UI/UX)
├── setup.sh              # Quick deployment script
├── core/
│   ├── __init__.py
│   ├── config.py         # Global settings & System Prompts
│   ├── agent.py          # RAG Reasoning Engine
│   └── embedder.py       # Vector Embedding Logic
├── tools/
│   ├── __init__.py
│   ├── pubmed.py         # PubMed Central API Integration
│   ├── web_search.py     # Tavily Web Search Engine
│   ├── graph.py          # Neo4j Cypher Query Generator
│   └── vector_db.py      # ChromaDB Vector Store
├── tests/                # Unit & Integration Tests
│   ├── test_agent.py
│   └── test_pubmed.py
└── data/                 # Local datasets & cache

```

---

## 🛠️ Key Features

* **Hybrid Knowledge Engine:** Merges **Graph Database** (Neo4j) for rigid facts with **Vector Store** (ChromaDB) for semantic nuances.
* **Live PubMed Integration:** Automatically fetches the latest abstracts to ensure the AI's knowledge is never outdated.
* **Triple-Tab Evidence:** Separates findings into `Graph`, `PubMed`, and `Web` for maximum transparency and peer review.
* **Bilingual Precision:** Specialized for Arabic-speaking scientists while maintaining English technical terminology.
* **Automated Seeding:** Built-in logic to populate Neo4j with a medical knowledge base seed on the first run.

---

## 🚀 Getting Started

### 1. Requirements

* Python 3.9+
* Neo4j Instance 
* OpenRouter or OpenAI API Key

### 2. Installation

```bash
git clone https://github.com/YourUsername/DrugDiscoveryRAG.git
cd DrugDiscoveryRAG
pip install -r requirements.txt

```

### 3. Configuration

Create a `.env` file:

```env
OPENROUTER_API_KEY=your_key
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=your_password
TAVILY_API_KEY=your_key

```

### 4. Running the Project

**Start the Backend (FastAPI):**

```bash
python main.py

```

**Start the Frontend (Streamlit):**

```bash
streamlit run app.py

```

---

## 🛡️ Disclaimer

> **Research Use Only:** This tool is designed for educational and research purposes. It is not a substitute for professional medical advice, diagnosis, or treatment.

**Developed with ❤️ for the BioTech AI Community.**
