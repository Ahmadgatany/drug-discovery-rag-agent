# 🧬 Drug Discovery AI Agent (Advanced Graph RAG System)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)
[![Neo4j](https://img.shields.io/badge/Neo4j-GraphDB-blue.svg)](https://neo4j.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-orange.svg)](https://www.trychroma.com/)

A sophisticated AI-driven Drug Discovery Explorer leveraging **Graph RAG** architecture. This system unifies structured Knowledge Graphs (Neo4j), semantic vector search (ChromaDB/PubMed), and real-time web intelligence (Tavily) to provide high-fidelity, cited analysis of drugs, genes, and molecular pathways.

---

## 🚀 Project Concept: The Power of Graph RAG

In the pharmaceutical domain, information is often fragmented. Traditional RAG (Vector-only) often fails to capture the complex, interconnected nature of biological data. This project implements a **Graph-Augmented Retrieval (Graph RAG)** approach to ensure:

1. **Relational Accuracy:** Unlike simple text matching, our Graph RAG tracks "Drug-Target-Disease" relationships as structured paths in Neo4j, preventing logical hallucinations.
2. **Contextual Synthesis:** It bridges gaps by parallel fetching data from a **Knowledge Graph**, **Vector Store** (PubMed), and **Live Web Search**.
3. **Multi-Hop Reasoning:** The agent can reason across diverse data types using **Llama 3.3**, answering complex questions by traversing graph nodes and grounding them with 2024-2025 clinical updates.

---

## 🏗️ System Architecture

The architecture is built on four specialized layers:

* **Knowledge Graph (Neo4j):** Stores rigid, verified relationships between drugs, targets (genes/proteins), and diseases.
* **Vector Database (ChromaDB):** Indexes semantic embeddings of PubMed abstracts for local, high-speed literature retrieval.
* **Real-time Tools:** Direct integration with **PubMed API** and **Tavily Search** for fetching the latest clinical trial updates (2024-2025).
* **Orchestration (FastAPI):** The central hub managing tool execution and LLM communication.



---

## 🛠️ Key Features

- [x] **Hybrid Retrieval:** Combines Cypher queries (structured) with Semantic Search (unstructured).
- [x] **2025 Data Accuracy:** Real-time web integration captures papers and warnings published as recently as this month.
- [x] **Medical Citations:** Automatically organizes evidence into separate tabs (Graph, Literature, Web) for transparency.
- [x] **Advanced UI:** A professional Streamlit dashboard with custom CSS for a medical-grade user experience.
- [x] **Automated Seeding:** Built-in scripts to populate the Knowledge Graph with initial drug-target data on startup.

---

## 💻 Installation & Setup

### 1. Clone the Repository:
```bash
git clone https://github.com/Ahmadgatany/drug-discovery-rag-agent.git
cd drug-discovery-rag-agent

```

### 2. Install Dependencies:

```bash
pip install -r requirements.txt

```

### 3. Environment Configuration

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your_key_here
NEO4J_URI=bolt://localhost:7687
NEO4J_PASSWORD=your_password
TAVILY_API_KEY=your_key_here

```

### 4. Run the Application

Start the Backend:

```bash
python main.py

```

Start the Frontend:

```bash
streamlit run app.py

```

---

## 📊 Example Queries

* *"Compare the molecular mechanism of Metformin vs Sitagliptin."*
* *"Are there any 2024-2025 warnings for Semaglutide regarding kidney function?"*
* *"Show the gene target and common side effects for Empagliflozin."*

---

## 🛡️ Disclaimer
*This system is for research purposes only. AI analysis should not replace professional medical judgment.*

**Developed with ❤️ for the BioTech AI Community.**

