import chromadb
from core.config import Config
from core.embedder import LocalEmbedder

class VectorTool:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.CHROMA_PATH)
        self.embedder = LocalEmbedder()
        self.collection = self.client.get_or_create_collection(
            name="drug_discovery_docs",
            metadata={"hnsw:space": "cosine"} # استخدام تشابه الجيوب لنتائج أدق
        )

    def add_texts(self, texts, metadatas=None):
        if not texts: 
            return
        
        embeddings = [self.embedder.encode(t) for t in texts]

        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]

        if metadatas is None:
            metadatas = [{"source": "pubmed_extract", "type": "scientific_paper"} for _ in texts]
        
        try:
            self.collection.add(
                documents=texts,
                embeddings=embeddings,
                metadatas=metadatas,
                ids=ids
            )
            print(f"[*] Successfully added {len(texts)} documents to ChromaDB.")
        except Exception as e:
            print(f"[!] ChromaDB Add Error: {e}")

    def search(self, query, n_results=3):
        query_embedding = self.embedder.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results
        )

        if results['documents']:
            return "\n\n".join(results['documents'][0])
        return "No relevant local literature found."