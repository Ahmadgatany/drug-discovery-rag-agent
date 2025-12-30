# 🧬 Drug Discovery AI Agent (Multi-Source RAG System)

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-UI-red.svg)](https://streamlit.io/)
[![Neo4j](https://img.shields.io/badge/Neo4j-GraphDB-blue.svg)](https://neo4j.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-VectorDB-orange.svg)](https://www.trychroma.com/)

A sophisticated AI-driven Drug Discovery Explorer leveraging **Retrieval-Augmented Generation (RAG)**. This system unifies structured knowledge graphs, scientific literature (PubMed), and real-time web intelligence to provide high-fidelity, cited analysis of drugs, genes, and molecular pathways.

---

## 🚀 Project Concept

In the pharmaceutical domain, information is often fragmented across structured databases (Neo4j), vast repositories of research papers (PubMed), and rapidly evolving clinical updates on the web. 

This **Medical AI Agent** bridges these gaps by:
1.  **Retrieving:** Parallel fetching of data from a Knowledge Graph, Vector Store (Local PubMed index), and Live Web Search.
2.  **Synthesizing:** Utilizing **Llama 3.3 (via OpenRouter)** to reason across these diverse data types.
3.  **Grounding:** Preventing hallucinations by strictly anchoring the AI's response to the retrieved context, ensuring 2024-2025 data accuracy.

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

This system is designed for **educational and research purposes only**. The AI-generated analysis should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always verify findings with clinical experts.

---

**Developed with ❤️ for the BioTech AI Community.**

```

Would you like me to add a **"Future Roadmap"** section to this file (e.g., adding 3D protein structure visualization or support for clinical trial PDF uploads)?

```
