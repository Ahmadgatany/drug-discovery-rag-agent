import chromadb
from core.config import Config
from core.embedder import LocalEmbedder

class VectorTool:
    def __init__(self):
        # استخدام التخزين المستمر (Persistent) لحفظ البيانات في مجلد data/
        self.client = chromadb.PersistentClient(path=Config.CHROMA_PATH)
        self.embedder = LocalEmbedder()
        self.collection = self.client.get_or_create_collection(
            name="drug_discovery_docs",
            metadata={"hnsw:space": "cosine"} # استخدام تشابه الجيوب لنتائج أدق
        )

    def add_texts(self, texts, metadatas=None):
        if not texts: 
            return
        
        # تحويل النصوص لمتجهات باستخدام الـ GPU
        embeddings = [self.embedder.encode(t) for t in texts]
        
        # إنشاء IDs فريدة لكل نص لضمان عدم حدوث تضارب في قاعدة البيانات
        import uuid
        ids = [str(uuid.uuid4()) for _ in texts]
        
        # الحل: التأكد من أن الميتادات تحتوي على معلومة واحدة على الأقل (مثل المصدر)
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
        
        # دمج النتائج في نص واحد للسياق
        if results['documents']:
            return "\n\n".join(results['documents'][0])
        return "No relevant local literature found."